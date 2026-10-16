#!/usr/bin/env python3
"""
HELIOS EPC Event-Driven Multi-Agent Simulation Orchestrator (64-Agent Full Ecosystem).
Executes the full closed-loop pipeline for a simulation day:
  run_day -> pd_inbox -> triggers -> invoke -> apply_actions -> post_messages -> comm_report
Enforces:
  - Max 8 agents invoked per day (priority-scored across all 64 agents).
  - Persona file read on invoke.
  - Tailored domain-filtered state brief across all 12 departments (PMO, PLN, ENG, SCM, CON, QAQ, EHS, COM, TNC, ADM, SUB, EXT).
  - Strict JSON output format: {"messages": [...], "actions": [...]}.
  - Validates actions against authority_matrix.json and mutates project_state.json + Markdown registers.
  - Routes coded messages to 10 GitHub Channels (CH-01 #11 to CH-10 #20) and dual .md department mailboxes.
  - Appends to Communication_Log.csv and generates COMM_MATRIX.md.
Python Standard Library only (calls agy CLI for agent intelligence).
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

from engine.run_day import run_simulation_day
from engine.triggers import evaluate_triggers
from engine.apply_actions import process_agent_actions
from scripts.post_messages import post_message
from scripts.pd_inbox import check_pd_inbox
from scripts.comm_report import generate_comm_report
from scripts.comm_log import AGENT_DEPT

STATE_DIR = os.path.join(REPO_ROOT, "state")
AUTHORITY_PATH = os.path.join(REPO_ROOT, "engine", "authority_matrix.json")
SIM_CLOCK_PATH = os.path.join(REPO_ROOT, "scripts", "sim_clock.json")


def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def clean_json_response(raw_text):
    """Cleans up markdown code fences and extracts JSON object"""
    text = raw_text.strip()
    if "```" in text:
        m = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
        if m:
            text = m.group(1).strip()
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = text[start:end+1]
        try:
            return json.loads(candidate)
        except Exception:
            pass
    try:
        return json.loads(text)
    except Exception as e:
        print(f"JSON parse error: {e}\nRaw output:\n{raw_text}", file=sys.stderr)
        return {"messages": [], "actions": []}


def build_domain_brief(agent, state_snapshot):
    """Constructs rich, tailored domain-filtered state brief across all 12 departments."""
    agent_up = agent.upper()
    dept = AGENT_DEPT.get(agent_up, "PMO")
    day = state_snapshot["day"]
    weather = state_snapshot.get("weather", {})
    evm = state_snapshot.get("project_totals", {})
    wps = state_snapshot.get("work_packages", {})
    events = state_snapshot.get("active_events", [])

    lines = [
        f"SIMULATION DAY: {day:03d} | DATE: {state_snapshot.get('sim_date')} | MONTH: {state_snapshot.get('month')} | WEEK: {state_snapshot.get('week')}",
        f"AGENT: {agent_up} | DEPARTMENT: {dept}",
        f"WEATHER: {weather.get('summary', 'Clear')} ({weather.get('temp_c', 24)}°C, Wind {weather.get('wind_kmh', 12)} km/h, Productivity Factor: {weather.get('productivity_factor', 1.0)})",
        f"ACTIVE EVENTS: {', '.join(events) if events else 'None (Clean Baseline)'}",
        f"EVM PERFORMANCE: SPI={evm.get('spi', 1.0):.4f}, CPI={evm.get('cpi', 1.0):.4f}, BCWS=${evm.get('bcws_usd', 0.0):,.2f}, BCWP=${evm.get('bcwp_usd', 0.0):,.2f}, ACWP=${evm.get('acwp_usd', 0.0):,.2f}"
    ]

    # Department-specific telemetry across all 12 departments
    if dept == "PMO":
        lines.extend([
            "PMO & DOCUMENT CONTROL TELEMETRY:",
            f"  - Plant Scope: 100MW Solar PV + 33/220kV GSS, Bukhara Uzbekistan (Contract Price: ${evm.get('bac_usd', 85000000.0):,.2f})",
            f"  - Overall Progress: {evm.get('progress_pct', 0.0):.4f}% | SV: ${evm.get('sv_usd', 0.0):,.2f} | CV: ${evm.get('cv_usd', 0.0):,.2f}",
            f"  - Civil Design (WP-ENG-CIV): {wps.get('WP-ENG-CIV', {}).get('qc_accepted', 0)}% | Elec Design (WP-ENG-ELE): {wps.get('WP-ENG-ELE', {}).get('qc_accepted', 0)}%",
            f"  - Site Mobilization (WP-CON-MOB): {wps.get('WP-CON-MOB', {}).get('qc_accepted', 0)}% | Site Grading (WP-CON-CIV-GRD): {wps.get('WP-CON-CIV-GRD', {}).get('qc_accepted', 0)}%",
            "  - Governance Channels: CH-01 (#11 PD-EXEC), CH-02 (#12 PMO-PLN), CH-03..CH-10 (#13..#20)"
        ])
    elif dept == "PLN":
        lines.extend([
            "PROJECT CONTROLS, SCHEDULE & EVM TELEMETRY:",
            f"  - Progress Earned (BCWP): ${evm.get('bcwp_usd', 0.0):,.2f} of ${evm.get('bac_usd', 85000000.0):,.2f} ({evm.get('progress_pct', 0.0):.4f}%)",
            f"  - Planned Value (BCWS): ${evm.get('bcws_usd', 0.0):,.2f} | Actual Cost (ACWP): ${evm.get('acwp_usd', 0.0):,.2f}",
            f"  - Schedule Variance (SV): ${evm.get('sv_usd', 0.0):,.2f} | Cost Variance (CV): ${evm.get('cv_usd', 0.0):,.2f}",
            "  - Master Critical Path: 220kV GSS Substation & 125MVA MPT (0 days Total Float)",
            "  - PV Array Field Float: +45 days parallel float to COD (Day 504)",
            "  - Key Milestones (28d/month): M2 Mobilization (Day 56), M4 First Pile (Day 112), M6 First Module (Day 168), M15 MC (Day 420), M16 Energization (Day 448), M18 COD (Day 504)"
        ])
    elif dept == "ENG":
        lines.extend([
            "ENGINEERING & DESIGN TELEMETRY:",
            f"  - Civil & Structural Design (WP-ENG-CIV): Installed {wps.get('WP-ENG-CIV', {}).get('installed', 0)}% | QC Accepted {wps.get('WP-ENG-CIV', {}).get('qc_accepted', 0)}% | IFC Released: {wps.get('WP-ENG-CIV', {}).get('ifc_released', False)}",
            f"  - PV & Electrical Design (WP-ENG-ELE): Installed {wps.get('WP-ENG-ELE', {}).get('installed', 0)}% | QC Accepted {wps.get('WP-ENG-ELE', {}).get('qc_accepted', 0)}% | IFC Released: {wps.get('WP-ENG-ELE', {}).get('ifc_released', False)}",
            f"  - 220kV GSS & Protection Design (WP-ENG-SUB): Installed {wps.get('WP-ENG-SUB', {}).get('installed', 0)}% | QC Accepted {wps.get('WP-ENG-SUB', {}).get('qc_accepted', 0)}% | IFC Released: {wps.get('WP-ENG-SUB', {}).get('ifc_released', False)}",
            f"  - Piling Workfront (WP-CON-CIV-PIL): {wps.get('WP-CON-CIV-PIL', {}).get('installed', 0)} / 15,400 piles installed"
        ])
    elif dept == "SCM":
        lines.extend([
            "SUPPLY CHAIN, PROCUREMENT & LOGISTICS TELEMETRY:",
            f"  - Bifacial TOPCon Modules (WP-PROC-MOD): Stage='{wps.get('WP-PROC-MOD', {}).get('milestone_stage')}' | Delivered: {wps.get('WP-PROC-MOD', {}).get('delivered', 0)} / 181,818 modules",
            f"  - 1P Single-Axis Trackers (WP-PROC-TRK): Stage='{wps.get('WP-PROC-TRK', {}).get('milestone_stage')}' | Delivered: {wps.get('WP-PROC-TRK', {}).get('delivered', 0)} / 2,200 tables",
            f"  - 125MVA 220/33kV MPT (WP-PROC-TRA): Stage='{wps.get('WP-PROC-TRA', {}).get('milestone_stage')}' | Critical Path 36-week lead time (PO drop-dead Day 45)",
            f"  - Central PCS / Inverters (WP-PROC-INV): Stage='{wps.get('WP-PROC-INV', {}).get('milestone_stage')}' | Scope: 25 units (4MW each)",
            f"  - 220kV GIS & HV Switchgear (WP-PROC-GIS): Stage='{wps.get('WP-PROC-GIS', {}).get('milestone_stage')}' | Scope: 1 lot"
        ])
    elif dept in ["CON", "SUB"]:
        lines.extend([
            "CONSTRUCTION & SUBCONTRACTOR WORKFRONT TELEMETRY:",
            f"  - Site Mobilization & Camp (WP-CON-MOB): {wps.get('WP-CON-MOB', {}).get('qc_accepted', 0)}% complete",
            f"  - Site Clearing & Grading (WP-CON-CIV-GRD): {wps.get('WP-CON-CIV-GRD', {}).get('qc_accepted', 0)}% complete",
            f"  - Pile Ramming (WP-CON-CIV-PIL): Delivered={wps.get('WP-CON-CIV-PIL', {}).get('delivered', 0)} | Installed={wps.get('WP-CON-CIV-PIL', {}).get('installed', 0)} | QC Accepted={wps.get('WP-CON-CIV-PIL', {}).get('qc_accepted', 0)} / 15,400 piles | IFC={wps.get('WP-CON-CIV-PIL', {}).get('ifc_released', False)}",
            f"  - Tracker Assembly (WP-CON-MEC-TRK): Installed={wps.get('WP-CON-MEC-TRK', {}).get('installed', 0)} / 2,200 tables",
            f"  - Module Mounting (WP-CON-MEC-MOD): Installed={wps.get('WP-CON-MEC-MOD', {}).get('installed', 0)} / 181,818 modules",
            f"  - DC/MV Cabling (WP-CON-ELE-CAB): {wps.get('WP-CON-ELE-CAB', {}).get('qc_accepted', 0)}% | 220kV GSS Erection (WP-CON-SUB-EREC): {wps.get('WP-CON-SUB-EREC', {}).get('qc_accepted', 0)}%"
        ])
    elif dept == "QAQ":
        lines.extend([
            "QUALITY ASSURANCE & ITP HOLD POINT TELEMETRY:",
            f"  - Active ITP Holds Logged: {len(state_snapshot.get('itp_holds', []))}",
            f"  - Open NCRs Logged: {len(state_snapshot.get('ncr_log', []))}",
            f"  - Piling QC Accepted vs Installed: {wps.get('WP-CON-CIV-PIL', {}).get('qc_accepted', 0)} / {wps.get('WP-CON-CIV-PIL', {}).get('installed', 0)} piles",
            "  - Rule: Zero earned value (BCWP) accrues on unaccepted work or active Hold Points."
        ])
    elif dept == "EHS":
        lines.extend([
            "EHS, SANPIN THERMAL & PERMIT-TO-WORK TELEMETRY:",
            f"  - Ambient Temp: {weather.get('temp_c', 24)}°C | Wind Speed: {weather.get('wind_kmh', 12)} km/h (Crane/Tracker lift limit: 35 km/h; Uzbek SanPiN thermal curtailment >42°C)",
            f"  - Active PTWs / Safety Holds in State: {len(state_snapshot.get('ptw_log', []))}",
            "  - Zero-LTI Target: Strict LOTO, excavation benching, and geotechnical drilling PTW enforcement active."
        ])
    elif dept == "COM":
        lines.extend([
            "CONTRACTS, CLAIMS, BILLING & COST CONTROL TELEMETRY:",
            "  - Governing Contract: FIDIC Yellow Book 1999 | Lump Sum Contract Price: $85,000,000.00",
            f"  - EVM Cost Metrics: CPI={evm.get('cpi', 1.0):.4f}, BCWP=${evm.get('bcwp_usd', 0.0):,.2f}, ACWP=${evm.get('acwp_usd', 0.0):,.2f}, CV=${evm.get('cv_usd', 0.0):,.2f}",
            f"  - FIDIC Notices Issued: {len(state_snapshot.get('fidic_notices', []))}",
            "  - Statutory Bar: Sub-Clause 20.1 strictly enforces a 28-day notice window from Contractor awareness; Sub-Clause 4.12 governs Unforeseeable Physical Conditions."
        ])
    elif dept == "TNC":
        lines.extend([
            "TESTING, COMMISSIONING & GRID COMPLIANCE TELEMETRY:",
            f"  - Cold & Hot Commissioning (WP-TNC-COM): {wps.get('WP-TNC-COM', {}).get('qc_accepted', 0)}% complete",
            f"  - Grid Code & Reliability Run (WP-TNC-GRID): {wps.get('WP-TNC-GRID', {}).get('qc_accepted', 0)}% complete",
            "  - Key Grid Requirements: UZBEKENERGO SCADA IEC 60870-5-104 point-to-point, PFR droop response, LVRT/HVRT, 72-hr reliability run, PR >= 81.5%."
        ])
    elif dept == "ADM":
        lines.extend([
            "SITE ADMINISTRATION, PERMITS & COMMUNITY LIAISON TELEMETRY:",
            f"  - Camp & Mobilization Progress (WP-CON-MOB): {wps.get('WP-CON-MOB', {}).get('qc_accepted', 0)}%",
            "  - Regulatory Scope: Bukhara regional construction permits, customs/visa clearances, camp welfare, and 70% local labor quota tracking."
        ])
    elif dept == "EXT":
        lines.extend([
            "EXTERNAL STAKEHOLDER & COUNTERPARTY INTERFACE TELEMETRY:",
            f"  - Counterparty Role: {agent_up} interfacing with HELIOS EPC Contractor via formal coded channels.",
            f"  - Reported Project Progress: {evm.get('progress_pct', 0.0):.4f}% | Active Events: {', '.join(events) if events else 'None'}",
            f"  - Formal Notices Received: {len(state_snapshot.get('fidic_notices', []))} | Open RFIs/FDCs: {len(state_snapshot.get('rfi_tq_fdc_log', []))}"
        ])

    if "EVT-001" in events:
        lines.append(
            "  - [ALERT EVT-001]: Unexpected subsurface basalt/caliche rock refusal encountered at 0.8m depth in Array Block 6 "
            "(tender baseline assumed 1.5m drive depth). Piling in Block 6 is held pending geotechnical investigation, FDC-CIV-001 pre-drilling design, and FIDIC Cl. 20.1/4.12 notice."
        )

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

=== YOUR PERSONA & INSTRUCTIONS ===
{persona_content[:3500]}

=== YOUR AUTHORITY & LIMITS ===
- Escalation Target: {agent_auth.get('escalation_target', 'ATLAS')}
- Financial Limit: {agent_auth.get('financial_limit', 'ESCALATE')}
- Allowed Actions: {json.dumps(agent_auth.get('allowed_actions', []))}
- Prohibitions: {json.dumps(agent_auth.get('prohibitions', []))}

=== CURRENT PROJECT STATE BRIEF (DAY {state_snapshot['day']:03d}) ===
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
      "work_code": "MOB|CIV|PIL|TRK|MOD|CAB|INV|FND|SUB|TRA|GIS|TNC|GEN",
      "type": "TYPE_CODE (INS|RFI|NCR|DEL|NTC|VO|BIL|RPT|ESC|EVT|MOM|INF)",
      "priority": "low|med|high|critical",
      "subject": "Clear subject summary",
      "body": "Rigorous, concise message body. Cite exact figures from brief; NEVER invent quantities.",
      "action_by_day": {state_snapshot['day'] + 1},
      "parent_msg_id": "optional parent msg-id from Inbox Items if replying, else empty"
    }}
  ],
  "actions": [
    {{
      "type": "action_type_code (e.g. issue_fdc, put_hold, log_delay_event, issue_notice, raise_ncr, issue_ptw, compile_dpr)",
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


def run_pilot_day(sim_day=2):
    """
    Executes the full event-driven agent loop for sim_day.
    """
    print(f"\n=======================================================")
    print(f"   HELIOS EPC SIMULATION ENGINE — DAY {sim_day:03d}")
    print(f"=======================================================\n")

    # Step A: run_day
    print(f"1. Advancing State Engine to Day {sim_day:03d}...")
    day_res, new_state = run_simulation_day(sim_day, write_state=True)
    print(f"   State Engine computed: SPI={day_res['spi']:.4f}, CPI={day_res['cpi']:.4f}, Piles={day_res['piles']}, Modules={day_res['modules']}")

    # Step B: pd_inbox
    print(f"\n2. Checking PD Inbox on Issue #11...")
    danesh_injections = check_pd_inbox()
    print(f"   Danesh direct commands: {len(danesh_injections)}")

    # Step C: triggers
    print(f"\n3. Evaluating Invocation Triggers across 64-Agent Roster...")
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

        # Step E: apply_actions (validates & mutates registers + project_state.json)
        actions = parsed_json.get("actions", [])
        if actions:
            acc, rej = process_agent_actions(sim_day, agent_name, actions, new_state)
            all_accepted_actions.extend(acc)
            all_rejected_actions.extend(rej)

        # Step F: post_messages (posts to GitHub CH-01..CH-10, Communication_Log.csv, and .md mailboxes)
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
            w_code = msg.get("work_code")

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
                cc_agents=cc_list,
                work_code=w_code
            )
            all_posted_messages.append(post_res)

    # Step G: comm_report
    print(f"\n5. Generating Communication Matrix Report...")
    generate_comm_report()

    # Step H: advance sim_clock.json
    print(f"\n6. Updating Sim Clock to Day {sim_day:03d} Complete...")
    clock_data = {
        "day": sim_day,
        "month": (sim_day - 1) // 28 + 1,
        "week": (sim_day - 1) // 7 + 1,
        "week_day": (sim_day - 1) % 7 + 1,
        "sim_date": new_state.get("sim_date"),
        "status": f"Day {sim_day} complete",
        "last_advanced_real_ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
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

    print(f"\nSimulation Day {sim_day:03d} execution complete. Summary saved to {out_pilot_path}\n")
    return pilot_summary


if __name__ == "__main__":
    day = 2
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        day = int(sys.argv[1])
    run_pilot_day(day)
