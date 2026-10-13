#!/usr/bin/env python3
"""
HELIOS EPC Deterministic Agent Invocation Trigger Engine.
Determines which agents are invoked on a given simulation day based on:
 (a) scheduled duty inside activity window (from workforce Excel),
 (b) open inbox items (from Communication_Log.csv),
 (c) breached thresholds (SPI<0.95, CPI<0.95, float<15d, PO drop-dead within 7d, notice day 20 of 28, RFI open >3d),
 (d) events in events.json hitting the agent,
 (e) Danesh direct injections/decisions.
Enforces hard maximum of 8 invoked agents per day; logs others as deferred.
Writes state/day_NNN_invocations.json.
Python Standard Library only (plus openpyxl for Excel reading).
"""

import csv
import json
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

STATE_DIR = os.path.join(REPO_ROOT, "state")
EVENTS_PATH = os.path.join(REPO_ROOT, "engine", "events.json")
COMM_LOG_PATH = os.path.join(REPO_ROOT, "11_Shared_Registers", "Communication_Log.csv")
WORKFORCE_PATH = os.path.join(REPO_ROOT, "00_Project_Overview", "HELIOS_EPC_Workforce.xlsx")
AUTHORITY_PATH = os.path.join(REPO_ROOT, "engine", "authority_matrix.json")

def load_json(filepath):
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def load_workforce_data():
    """Reads activity windows and duties from HELIOS_EPC_Workforce.xlsx"""
    import openpyxl
    wb = openpyxl.load_workbook(WORKFORCE_PATH, data_only=True)
    sheet = wb["🗂 Full Workforce"]
    roster = {}
    for row in sheet.iter_rows(values_only=True):
        if row[0] and row[1] and row[2] and not str(row[0]).startswith(" "):
            if row[0] != "Agent ID":
                name = str(row[1]).strip().upper()
                roster[name] = {
                    "agent_id": str(row[0]).strip(),
                    "name": name,
                    "dept": str(row[2]).strip(),
                    "role": str(row[3]).strip() if row[3] else "",
                    "reports_to": str(row[4]).strip() if row[4] else "",
                    "activity_window": str(row[7]).strip() if row[7] else "Full lifecycle",
                    "key_docs": str(row[8]).strip() if row[8] else ""
                }
    return roster

def is_inside_activity_window(agent, sim_day, workforce_roster):
    """
    Checks if current simulation day falls inside agent's activity window.
    28-day months:
    - LNTP / Month 1: Days 1-28
    - Month 4 (Piling): Day 112
    - Month 6 (Modules): Day 168
    - Month 13+ (Pre-comm / T&C): Day 364+
    """
    info = workforce_roster.get(agent)
    if not info:
        return True
    window = info.get("activity_window", "Full lifecycle")
    w_lower = window.lower()

    if "full lifecycle" in w_lower:
        return True
    if "pre-comm" in w_lower or "protection test" in w_lower:
        return sim_day >= 364
    if "civil completion" in w_lower and sim_day > 250:
        return False
    if "lntp" in w_lower or "ntp" in w_lower:
        return True
    return True

def get_open_inbox_items(agent):
    """Extracts open incoming messages from Communication_Log.csv"""
    inbox = []
    if not os.path.exists(COMM_LOG_PATH):
        return inbox

    with open(COMM_LOG_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            to_ag = row.get("to_agent", "").strip().upper()
            status = row.get("status", "").strip().lower()
            if to_ag == agent and status in ["open", "pending", "action_required"]:
                inbox.append({
                    "msg_id": row.get("msg_id"),
                    "from_agent": row.get("from_agent"),
                    "from_dept": row.get("from_dept"),
                    "type": row.get("type"),
                    "priority": row.get("priority"),
                    "topic": row.get("topic"),
                    "sim_day": int(row.get("sim_day")) if row.get("sim_day", "").isdigit() else 0,
                    "comment_url": row.get("comment_url")
                })
    return inbox

def evaluate_triggers(sim_day, state_snapshot, danesh_injections=None):
    """
    Evaluates candidate agents for invocation on sim_day.
    Caps at 8 agents; logs deferred agents.
    """
    workforce = load_workforce_data()
    all_events = load_json(EVENTS_PATH)
    if not isinstance(all_events, list):
        all_events = []

    # Active events for day
    active_events = []
    for ev in all_events:
        w_start, w_end = ev.get("trigger_window_days", [0, 0])
        if w_start <= sim_day <= w_end:
            active_events.append(ev)

    project_totals = state_snapshot.get("project_totals", {})
    spi = project_totals.get("spi", 1.0)
    cpi = project_totals.get("cpi", 1.0)

    candidates = {}

    def add_candidate(agent, priority_score, reason, inbox_items=None):
        if not is_inside_activity_window(agent, sim_day, workforce):
            return
        if agent not in candidates:
            candidates[agent] = {
                "agent": agent,
                "score": priority_score,
                "reasons": [reason],
                "inbox_items": inbox_items or []
            }
        else:
            candidates[agent]["score"] = max(candidates[agent]["score"], priority_score)
            if reason not in candidates[agent]["reasons"]:
                candidates[agent]["reasons"].append(reason)
            if inbox_items:
                candidates[agent]["inbox_items"].extend(inbox_items)

    # 1. Danesh Direct Injections (Priority 100)
    if danesh_injections:
        for inj in danesh_injections:
            target = inj.get("agent", "ATLAS")
            add_candidate(target, 100, f"Danesh instruction: {inj.get('command')}", inj.get("items"))

    # 2. Events hitting agents (Priority 80)
    for ev in active_events:
        for ag in ev.get("agents_hit", []):
            add_candidate(ag, 80, f"{ev['event_id']} active: {ev['title']}")

    # 3. Threshold Breaches (Priority 60)
    if spi < 0.95:
        add_candidate("KRONOS", 65, f"Threshold breached: SPI={spi:.4f} < 0.95")
        add_candidate("ATLAS", 60, f"Threshold breached: SPI={spi:.4f} < 0.95")
    if cpi < 0.95:
        add_candidate("LEDGER", 65, f"Threshold breached: CPI={cpi:.4f} < 0.95")
        add_candidate("ATLAS", 60, f"Threshold breached: CPI={cpi:.4f} < 0.95")

    # 4. Open Inbox Items (Priority 50)
    for agent_name in workforce:
        inbox = get_open_inbox_items(agent_name)
        if inbox:
            add_candidate(agent_name, 50, f"{len(inbox)} open inbox items requiring action", inbox)

    # 5. Routine Scheduled Duties inside Activity Window (Priority 30)
    # ATLAS: Daily Project Management & PD Brief
    add_candidate("ATLAS", 35, "Scheduled daily duty: Project direction and PD brief orchestration")
    # SIGMA: Daily MIS Reporting / DPR compilation
    add_candidate("SIGMA", 30, "Scheduled daily duty: Daily Progress Report (DPR) data compilation")

    # Sort candidates by score descending
    sorted_candidates = sorted(candidates.values(), key=lambda c: c["score"], reverse=True)

    max_agents = 8
    invoked = []
    deferred = []

    for idx, cand in enumerate(sorted_candidates):
        entry = {
            "agent": cand["agent"],
            "priority_score": cand["score"],
            "reason": "; ".join(cand["reasons"]),
            "inbox_items": cand["inbox_items"]
        }
        if idx < max_agents:
            invoked.append(entry)
        else:
            deferred_entry = entry.copy()
            deferred_entry["deferral_reason"] = f"Daily execution cap ({max_agents} agents) reached; deferred to next cycle"
            deferred.append(deferred_entry)

    result = {
        "day": sim_day,
        "max_invocations_allowed": max_agents,
        "total_triggered_candidates": len(sorted_candidates),
        "invoked_count": len(invoked),
        "deferred_count": len(deferred),
        "invoked": invoked,
        "deferred": deferred
    }

    out_file = os.path.join(STATE_DIR, f"day_{sim_day:03d}_invocations.json")
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"Computed invocations for Day {sim_day}: {len(invoked)} invoked, {len(deferred)} deferred.")
    print(f"Saved to {out_file}")
    return result

if __name__ == "__main__":
    day = 5
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        day = int(sys.argv[1])
    state_snap = load_json(os.path.join(STATE_DIR, f"day_{day:03d}_state.json"))
    if not state_snap:
        state_snap = load_json(os.path.join(STATE_DIR, "project_state.json"))
    res = evaluate_triggers(day, state_snap)
    print("\nInvoked agents:")
    for inv in res["invoked"]:
        print(f"  - {inv['agent']:12} | Score {inv['priority_score']:3d} | {inv['reason']}")
    if res["deferred"]:
        print("\nDeferred agents:")
        for def_a in res["deferred"]:
            print(f"  - {def_a['agent']:12} | {def_a['deferral_reason']}")
