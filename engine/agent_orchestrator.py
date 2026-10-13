#!/usr/bin/env python3
"""
HELIOS EPC Event-Driven Multi-Agent Simulation Orchestrator.
Executes the full pipeline for a simulation day:
  run_day -> pd_inbox -> triggers -> invoke -> apply_actions -> post_messages -> comm_report
Enforces:
  - Max 8 agents invoked per day.
  - Persona file read on invoke.
  - Domain-filtered state brief.
  - Strict JSON output format: {"messages": [...], "actions": [...]}.
  - Validates actions against authority_matrix.json.
  - Posts to GitHub issues (Issue #11 for ATLAS PD briefs, topic threads for others).
  - Appends to Communication_Log.csv and generates COMM_MATRIX.md.
Python Standard Library only (calls agy CLI for agent intelligence).
"""

import copy
import json
import os
import re
import subprocess
import sys
from datetime import datetime

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

from engine.run_day import run_simulation_day
from engine.triggers import evaluate_triggers
from engine.apply_actions import process_agent_actions
from scripts.post_messages import post_message
from scripts.pd_inbox import check_pd_inbox
from scripts.comm_report import generate_comm_report

STATE_DIR = os.path.join(REPO_ROOT, "state")
AUTHORITY_PATH = os.path.join(REPO_ROOT, "engine", "authority_matrix.json")
SIM_CLOCK_PATH = os.path.join(REPO_ROOT, "scripts", "sim_clock.json")

def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def clean_json_response(raw_text):
    """Cleans up markdown code fences and extracts JSON object"""
    text = raw_text.strip()
    # Remove markdown code fence if present
    m = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
    if m:
        text = m.group(1).strip()
    else:
        # Look for first { to last }
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            text = text[start:end+1]
    try:
        return json.loads(text)
    except Exception as e:
        print(f"JSON parse error: {e}\nRaw output:\n{raw_text}", file=sys.stderr)
        return {"messages": [], "actions": []}

def build_domain_brief(agent, state_snapshot):
    """Constructs domain-filtered state brief for agent"""
    day = state_snapshot["day"]
    weather = state_snapshot.get("weather", {})
    evm = state_snapshot.get("project_totals", {})
    wps = state_snapshot.get("work_packages", {})
    events = state_snapshot.get("active_events", [])

    lines = [
        f"SIMULATION DAY: {day} | DATE: {state_snapshot.get('sim_date')} | MONTH: {state_snapshot.get('month')}",
        f"WEATHER: {weather.get('summary', 'Clear')} (Productivity factor: {weather.get('productivity_factor', 1.0)})",
        f"ACTIVE EVENTS: {', '.join(events) if events else 'None'}",
        f"EVM PERFORMANCE: SPI={evm.get('spi', 1.0):.4f}, CPI={evm.get('cpi', 1.0):.4f}, BCWS=${evm.get('bcws_usd', 0.0):,.2f}, BCWP=${evm.get('bcwp_usd', 0.0):,.2f}, ACWP=${evm.get('acwp_usd', 0.0):,.2f}"
    ]

    # Domain specific data
    if agent in ["TERRA", "MERIDIAN", "BASTION", "RAMPART", "GROUNDWORK"]:
        lines.append("CIVIL & STRUCTURAL WORKFRONT STATUS:")
        lines.append(f"  - PV Field Piling (WP-CON-CIV-PIL): Scope 15,400 piles | Delivered: {wps.get('WP-CON-CIV-PIL', {}).get('delivered')} | Installed: {wps.get('WP-CON-CIV-PIL', {}).get('installed')} | QC Accepted: {wps.get('WP-CON-CIV-PIL', {}).get('qc_accepted')} | IFC: {wps.get('WP-CON-CIV-PIL', {}).get('ifc_released')}")
        lines.append(f"  - Site Grading (WP-CON-CIV-GRD): Scope 100% | Installed: {wps.get('WP-CON-CIV-GRD', {}).get('installed')}% | QC Accepted: {wps.get('WP-CON-CIV-GRD', {}).get('qc_accepted')}%")
        lines.append(f"  - Civil Design (WP-ENG-CIV): Design Progress {wps.get('WP-ENG-CIV', {}).get('installed')}% | QC Accepted: {wps.get('WP-ENG-CIV', {}).get('qc_accepted')}%")
        if "EVT-001" in events:
            lines.append("  - EVENT EVT-001: Geotechnical rock refusal encountered at 0.8m depth in Array Block 6 (tender design assumed 1.5m). Piling in Block 6 is blocked; pre-drilling or foundation redesign required.")

    elif agent in ["KRONOS", "SIGMA", "VECTOR", "WATT", "LEDGER"]:
        lines.append("PROJECT CONTROLS & SCHEDULE METRICS:")
        lines.append(f"  - Progress Earned: ${evm.get('bcwp_usd', 0.0):,.2f} of ${evm.get('bac_usd', 85000000.0):,.2f} ({evm.get('progress_pct', 0.0):.3f}%)")
        lines.append(f"  - Schedule Variance: ${evm.get('sv_usd', 0.0):,.2f} | Cost Variance: ${evm.get('cv_usd', 0.0):,.2f}")
        lines.append("  - Critical Path: Main Power Transformer (MPT) & 220kV GSS Substation (0d Float)")
        lines.append("  - Milestones: Mobilization M2 (Day 56), First Pile M4 (Day 112), First Module Delivery M6 (Day 168)")

    elif agent in ["COUNSEL", "CLAIMS", "INVOICE", "CHECKER", "LEDGE"]:
        lines.append("CONTRACT & COMMERCIAL STATUS:")
        lines.append("  - Contract: FIDIC Yellow Book 1999, Contract Price USD 85,000,000")
        lines.append("  - Notice Window: Sub-Clause 20.1 requires formal notice within 28 days of Contractor awareness.")
        lines.append("  - Sub-Clause 4.12: Unforeseeable Physical Conditions entitlement for Block 6 rock refusal.")

    elif agent == "ATLAS":
        lines.append("EXECUTIVE PROJECT STATUS:")
        lines.append(f"  - Plant Scope: 100MW Solar PV + 33/220kV GSS, Bukhara Uzbekistan")
        lines.append(f"  - Day {day} Operations: Early engineering design & site mobilization underway.")
        lines.append(f"  - Active Alert: EVT-001 rock layer refusal at 0.8m in Block 6 requires cross-department coordination.")

    return "\n".join(lines)

def invoke_agent(agent_name, invocation_reason, inbox_items, state_snapshot):
    """
    Invokes an agent using agy CLI non-interactive mode.
    Reads persona file, filters brief, provides authority matrix, and extracts JSON output.
    """
    authority_matrix = load_json(AUTHORITY_PATH)
    agent_auth = authority_matrix.get(agent_name, {})
    persona_path = os.path.join(REPO_ROOT, agent_auth.get("file", ""))

    persona_content = ""
    if os.path.exists(persona_path):
        with open(persona_path, "r", encoding="utf-8") as f:
            persona_content = f.read()
    else:
        persona_content = f"Role: {agent_auth.get('role', agent_name)}"

    domain_brief = build_domain_brief(agent_name, state_snapshot)

    prompt = f"""You are AI agent **{agent_name}** in the HELIOS 100MW Solar PV EPC simulation (FIDIC Yellow Book).
Act strictly according to your assigned role, professional discipline, and authority limits.

=== YOUR AUTHORITY & LIMITS ===
- Escalation Target: {agent_auth.get('escalation_target', 'ATLAS')}
- Financial Limit: {agent_auth.get('financial_limit', 'ESCALATE')}
- Allowed Actions: {json.dumps(agent_auth.get('allowed_actions', []))}
- Prohibitions: {json.dumps(agent_auth.get('prohibitions', []))}

=== CURRENT PROJECT STATE BRIEF (DAY {state_snapshot['day']}) ===
{domain_brief}

=== TRIGGER & INBOX ITEMS ===
Trigger Reason: {invocation_reason}
Inbox Items: {json.dumps(inbox_items, indent=2)}

=== OUTPUT INSTRUCTIONS ===
You must respond with a SINGLE valid JSON object ONLY.
NO markdown code fences, NO explanation, NO conversational prose.
JSON Schema:
{{
  "messages": [
    {{
      "to": "RECIPIENT_AGENT_NAME",
      "cc": ["CC_AGENT_NAME"],
      "type": "TYPE_CODE (INS|RFI|NCR|DEL|NTC|VO|BIL|RPT|ESC|EVT|MOM|INF)",
      "priority": "low|med|high|critical",
      "subject": "Clear subject summary",
      "body": "Rigorous, concise message body. Cite exact figures from brief; NEVER invent quantities.",
      "action_by_day": {state_snapshot['day'] + 1},
      "parent_msg_id": "optional parent msg-id or empty"
    }}
  ],
  "actions": [
    {{
      "type": "action_type_code (e.g. issue_fdc, log_delay_event, issue_notice, compile_dpr, put_hold)",
      "params": {{"key": "value"}}
    }}
  ]
}}
"""

    print(f"Calling agent {agent_name} via agy...")
    cmd = ["agy", "-p", prompt]
    res = subprocess.run(cmd, capture_output=True, text=True)
    raw_output = res.stdout.strip()
    if res.returncode != 0:
        print(f"Agent {agent_name} returned code {res.returncode}: {res.stderr}", file=sys.stderr)

    parsed_json = clean_json_response(raw_output)
    return parsed_json, raw_output

def run_pilot_day(sim_day=5):
    """
    Executes the full event-driven agent pilot for sim_day.
    """
    print(f"\n=======================================================")
    print(f"   HELIOS EPC SIMULATION PILOT — DAY {sim_day:03d}")
    print(f"=======================================================\n")

    # Step A: run_day
    print(f"1. Advancing State Engine to Day {sim_day}...")
    day_res, new_state = run_simulation_day(sim_day, write_state=True)
    print(f"   State Engine computed: SPI={day_res['spi']:.4f}, CPI={day_res['cpi']:.4f}, Piles={day_res['piles']}, Modules={day_res['modules']}")

    # Step B: pd_inbox
    print(f"\n2. Checking PD Inbox on Issue #11...")
    danesh_injections = check_pd_inbox()
    print(f"   Danesh direct commands: {len(danesh_injections)}")

    # Step C: triggers
    print(f"\n3. Evaluating Invocation Triggers...")
    triggers_res = evaluate_triggers(sim_day, new_state, danesh_injections=danesh_injections)
    invoked_list = triggers_res.get("invoked", [])
    deferred_list = triggers_res.get("deferred", [])
    print(f"   Invoked Agents ({len(invoked_list)}): {', '.join([i['agent'] for i in invoked_list])}")
    print(f"   Deferred Agents ({len(deferred_list)})")

    # Step D: invoke agents
    print(f"\n4. Invoking Agents (Agent Call Protocol)...")
    agent_outputs = {}
    all_accepted_actions = []
    all_rejected_actions = []
    all_posted_messages = []

    for inv in invoked_list:
        agent_name = inv["agent"]
        reason = inv["reason"]
        inbox = inv.get("inbox_items", [])

        parsed_json, raw_out = invoke_agent(agent_name, reason, inbox, new_state)
        agent_outputs[agent_name] = {
            "parsed": parsed_json,
            "raw": raw_out
        }

        # Step E: apply_actions
        actions = parsed_json.get("actions", [])
        if actions:
            acc, rej = process_agent_actions(sim_day, agent_name, actions, new_state)
            all_accepted_actions.extend(acc)
            all_rejected_actions.extend(rej)

        # Step F: post_messages
        messages = parsed_json.get("messages", [])
        for msg in messages:
            to_agent = msg.get("to", "ATLAS")
            msg_type = msg.get("type", "INF")
            prio = msg.get("priority", "med")
            subj = msg.get("subject", "Update")
            body = msg.get("body", "")
            action_by = msg.get("action_by_day", sim_day + 1)
            parent_id = msg.get("parent_msg_id", "")
            cc_list = msg.get("cc", [])

            post_res = post_message(
                from_agent=agent_name,
                to_agent=to_agent,
                msg_type=msg_type,
                priority=prio,
                subject=subj,
                body=body,
                sim_day=sim_day,
                action_by_day=action_by,
                parent_msg_id=parent_id,
                cc_agents=cc_list
            )
            all_posted_messages.append(post_res)

    # Step G: comm_report
    print(f"\n5. Generating Communication Matrix Report...")
    report_text = generate_comm_report()

    # Step H: advance sim_clock.json
    print(f"\n6. Updating Sim Clock to Day {sim_day} Complete...")
    clock_data = {
        "day": sim_day,
        "month": (sim_day - 1) // 28 + 1,
        "week": (sim_day - 1) // 7 + 1,
        "week_day": (sim_day - 1) % 7 + 1,
        "sim_date": new_state.get("sim_date"),
        "status": f"Day {sim_day} complete",
        "last_advanced_real_ts": datetime.now().isoformat()
    }
    with open(SIM_CLOCK_PATH, "w", encoding="utf-8") as f:
        json.dump(clock_data, f, indent=2)

    # Return summary dict
    pilot_summary = {
        "day": sim_day,
        "invoked": invoked_list,
        "deferred": deferred_list,
        "agent_outputs": agent_outputs,
        "accepted_actions": all_accepted_actions,
        "rejected_actions": all_rejected_actions,
        "posted_messages": all_posted_messages,
        "evm": new_state.get("project_totals", {})
    }

    out_pilot_path = os.path.join(STATE_DIR, f"day_{sim_day:03d}_pilot_results.json")
    with open(out_pilot_path, "w", encoding="utf-8") as f:
        json.dump(pilot_summary, f, indent=2)

    print(f"\nPilot Day {sim_day} execution complete. Summary saved to {out_pilot_path}\n")
    return pilot_summary

if __name__ == "__main__":
    day = 5
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        day = int(sys.argv[1])
    run_pilot_day(day)
