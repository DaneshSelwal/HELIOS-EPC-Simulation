#!/usr/bin/env python3
"""
HELIOS EPC Deterministic Simulation Daily State Transition Runner.
Computes site reality, material logistics, physical construction progress,
and EVM performance for a single simulation day.
Writes state/day_NNN_state.json and a read-only structured state brief.
NO narrative text or LLM hallucination. Python Standard Library only.
"""

import argparse
import copy
from datetime import datetime, timedelta
import json
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

from engine.site_reality import SiteRealityEngine
from engine.evm import EVMEngine

STATE_DIR = os.path.join(REPO_ROOT, "state")
EVENTS_PATH = os.path.join(REPO_ROOT, "engine", "events.json")
BASELINE_PATH = os.path.join(REPO_ROOT, "state", "baseline.json")
CURRENT_STATE_PATH = os.path.join(REPO_ROOT, "state", "project_state.json")

def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(filepath, data):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def get_active_events_for_day(sim_day, all_events):
    active = []
    for ev in all_events:
        w_start, w_end = ev.get("trigger_window_days", [0, 0])
        if w_start <= sim_day <= w_end:
            active.append(ev)
    return active

def get_evm_history_up_to(day, in_memory_history=None):
    if in_memory_history is not None:
        return in_memory_history
    history = []
    for d in range(1, day):
        snap_path = os.path.join(STATE_DIR, f"day_{d:03d}_state.json")
        if os.path.exists(snap_path):
            snap = load_json(snap_path)
            totals = snap.get("project_totals", {})
            history.append({
                "day": d,
                "bcwp": totals.get("bcwp_usd", 0.0),
                "spi": totals.get("spi", 1.0),
                "cpi": totals.get("cpi", 1.0)
            })
    return history

def run_simulation_day(target_day, prior_state=None, history=None, write_state=True):
    """
    Simulates transitions from Day (target_day - 1) to target_day.
    """
    baseline = load_json(BASELINE_PATH)
    all_events = load_json(EVENTS_PATH)

    # 1. Load starting state
    if prior_state is not None:
        current_state = prior_state
    else:
        prev_day = target_day - 1
        prev_snapshot_path = os.path.join(STATE_DIR, f"day_{prev_day:03d}_state.json")
        if os.path.exists(prev_snapshot_path):
            current_state = load_json(prev_snapshot_path)
        elif os.path.exists(CURRENT_STATE_PATH):
            current_state = load_json(CURRENT_STATE_PATH)
        else:
            raise FileNotFoundError(f"Cannot find prior state for Day {target_day}")

    new_state = copy.deepcopy(current_state)
    new_state["day"] = target_day

    # Sim date calculations
    start_date = datetime.strptime("2026-10-06", "%Y-%m-%d")
    current_date = start_date + timedelta(days=target_day - 1)
    new_state["sim_date"] = current_date.strftime("%Y-%m-%d")
    new_state["month"] = (target_day - 1) // 28 + 1
    new_state["week"] = (target_day - 1) // 7 + 1
    new_state["status"] = f"Day {target_day} complete"

    # 2. Site Reality & Weather
    reality_engine = SiteRealityEngine()
    weather = reality_engine.get_weather(target_day)
    active_events = get_active_events_for_day(target_day, all_events)

    # 3. Process Work Packages
    # A. Engineering Packages
    # Daily incremental progress for active design packages
    eng_daily_burn = {
        "WP-ENG-CIV": (0.85, 2600.0),  # (progress %, daily actual cost)
        "WP-ENG-ELE": (0.75, 2800.0),
        "WP-ENG-MEC": (0.70, 1500.0),
        "WP-ENG-SUB": (0.80, 1600.0)
    }

    for eng_id, (prog_rate, cost_rate) in eng_daily_burn.items():
        wp = new_state["work_packages"][eng_id]
        if wp["installed"] < 100.0:
            daily_p = prog_rate * weather["productivity_factor"]
            wp["installed"] = round(min(100.0, wp["installed"] + daily_p), 4)
            # QC accepted trails slightly behind design reviews
            wp["qc_accepted"] = round(min(wp["installed"], wp["qc_accepted"] + daily_p * 0.95), 4)
            wp["actual_cost"] = round(wp["actual_cost"] + cost_rate, 2)
            if wp["installed"] >= 100.0:
                wp["ifc_released"] = True

    # B. Procurement Packages & Awards
    # Handle PO drops and factory lead times
    if target_day == 12:
        # Day 12 milestone: Main Power Transformer (MPT) PO awarded
        mpt_wp = new_state["work_packages"].get("WP-PROC-TRA")
        if mpt_wp and not mpt_wp.get("po_issued"):
            mpt_wp["po_issued"] = {
                "day": 12,
                "lead_time": 182,  # 26 weeks
                "eta": 194
            }
            mpt_wp["committed"] = 1800000.0
            # 15% advance payment incurred
            mpt_wp["actual_cost"] = round(mpt_wp["actual_cost"] + 270000.0, 2)

    # Check for procurement deliveries
    for proc_id in ["WP-PROC-PIL", "WP-PROC-TRK", "WP-PROC-MOD", "WP-PROC-INV", "WP-PROC-TRA", "WP-PROC-GIS", "WP-PROC-CAB-DC", "WP-PROC-CAB-MV", "WP-PROC-BOP"]:
        wp = new_state["work_packages"].get(proc_id)
        if wp and wp.get("po_issued"):
            po = wp["po_issued"]
            if target_day >= po["eta"] and wp["delivered"] < wp["total_qty"]:
                wp["delivered"] = wp["total_qty"]
                wp["qc_accepted"] = round(wp["total_qty"] * 0.98, 2)

    # C. Construction Packages
    for con_id in ["WP-CON-MOB", "WP-CON-CIV-GRD", "WP-CON-CIV-PIL", "WP-CON-MEC-TRK", "WP-CON-MEC-MOD", "WP-CON-ELE-DC", "WP-CON-ELE-MV", "WP-CON-CIV-FND", "WP-CON-SUB-ERE"]:
        wp = new_state["work_packages"].get(con_id)
        if not wp:
            continue

        prod_qty, reason = reality_engine.compute_daily_production(con_id, new_state, weather, active_events)
        if prod_qty > 0.0:
            wp["installed"] = round(wp["installed"] + prod_qty, 2)
            # QC inspection passes 96% of daily production
            wp["qc_accepted"] = round(min(wp["installed"], wp["qc_accepted"] + prod_qty * 0.96), 2)
            # Incur daily unit installation cost
            unit_rate = (wp["budget"] / wp["total_qty"]) if wp["total_qty"] > 0 else 0.0
            # Actual cost includes equipment/labor overhead
            daily_cost = prod_qty * unit_rate * 1.02
            wp["actual_cost"] = round(wp["actual_cost"] + daily_cost, 2)

    # 4. EVM Calculation
    evm_engine = EVMEngine(BASELINE_PATH)
    hist = get_evm_history_up_to(target_day, in_memory_history=history)
    evm_metrics = evm_engine.calculate_evm(new_state, history=hist)

    new_state["project_totals"] = {
        "contract_price_usd": evm_metrics["bac"],
        "bac_usd": evm_metrics["bac"],
        "bcws_usd": evm_metrics["bcws"],
        "bcwp_usd": evm_metrics["bcwp"],
        "acwp_usd": evm_metrics["acwp"],
        "sv_usd": evm_metrics["sv"],
        "cv_usd": evm_metrics["cv"],
        "spi": evm_metrics["spi"],
        "cpi": evm_metrics["cpi"],
        "progress_pct": evm_metrics["progress_pct"]
    }
    new_state["discipline_performance"] = evm_metrics["discipline_performance"]
    new_state["weather"] = weather
    new_state["active_events"] = [e["event_id"] for e in active_events]

    # 5. Output Artifacts
    if write_state:
        # Write daily state snapshot
        snap_path = os.path.join(STATE_DIR, f"day_{target_day:03d}_state.json")
        save_json(snap_path, new_state)

        # Update live project_state.json
        save_json(CURRENT_STATE_PATH, new_state)

        # Write read-only state brief (No narrative text)
        brief_data = {
            "day": target_day,
            "sim_date": new_state["sim_date"],
            "month": new_state["month"],
            "week": new_state["week"],
            "weather": {
                "temp_c": weather["temp_c"],
                "wind_speed_ms": weather["wind_speed_ms"],
                "dust_storm": weather["dust_storm"],
                "productivity_factor": weather["productivity_factor"],
                "conditions": weather["summary"]
            },
            "active_events": [
                {"id": e["event_id"], "title": e["title"], "agents": e["agents_hit"]}
                for e in active_events
            ],
            "evm": {
                "bcws_usd": evm_metrics["bcws"],
                "bcwp_usd": evm_metrics["bcwp"],
                "acwp_usd": evm_metrics["acwp"],
                "spi": evm_metrics["spi"],
                "cpi": evm_metrics["cpi"],
                "progress_pct": evm_metrics["progress_pct"]
            },
            "physical_metrics": {
                "piles_installed": new_state["work_packages"]["WP-CON-CIV-PIL"]["installed"],
                "piles_qc_accepted": new_state["work_packages"]["WP-CON-CIV-PIL"]["qc_accepted"],
                "modules_installed": new_state["work_packages"]["WP-CON-MEC-MOD"]["installed"],
                "modules_qc_accepted": new_state["work_packages"]["WP-CON-MEC-MOD"]["qc_accepted"],
                "trackers_installed": new_state["work_packages"]["WP-CON-MEC-TRK"]["installed"],
                "mobilization_pct": new_state["work_packages"]["WP-CON-MOB"]["installed"]
            },
            "disciplines": evm_metrics["discipline_performance"]
        }
        brief_json_path = os.path.join(STATE_DIR, f"state_brief_Day{target_day:03d}.json")
        save_json(brief_json_path, brief_data)

        # Markdown format brief (tables and numbers only, no prose/narrative)
        brief_md_path = os.path.join(STATE_DIR, "STATE_BRIEF.md")
        md_lines = [
            f"# HELIOS EPC REALITY STATE BRIEF — DAY {target_day:03d}",
            f"- **Date**: {new_state['sim_date']} (Month {new_state['month']}, Week {new_state['week']})",
            f"- **Weather**: {weather['summary']}",
            f"- **Active Events**: {', '.join(new_state['active_events']) if new_state['active_events'] else 'None'}",
            "",
            "## 1. Earned Value Metrics",
            "| Metric | Value | Baseline Target | Variance | Status |",
            "|---|---|---|---|---|",
            f"| Planned Value (BCWS) | ${evm_metrics['bcws']:,.2f} | — | — | Baseline S-Curve |",
            f"| Earned Value (BCWP) | ${evm_metrics['bcwp']:,.2f} | ${evm_metrics['bcws']:,.2f} | ${evm_metrics['sv']:,.2f} | {'Ahead' if evm_metrics['sv']>=0 else 'Behind'} |",
            f"| Actual Cost (ACWP) | ${evm_metrics['acwp']:,.2f} | ${evm_metrics['bcwp']:,.2f} | ${evm_metrics['cv']:,.2f} | {'Under Budget' if evm_metrics['cv']>=0 else 'Over Budget'} |",
            f"| SPI | {evm_metrics['spi']:.4f} | 1.0000 | {evm_metrics['spi']-1.0:+.4f} | {'On/Ahead' if evm_metrics['spi']>=1.0 else 'Behind'} |",
            f"| CPI | {evm_metrics['cpi']:.4f} | 1.0000 | {evm_metrics['cpi']-1.0:+.4f} | {'Under/On' if evm_metrics['cpi']>=1.0 else 'Over'} |",
            "",
            "## 2. Key Physical Quantities",
            "| Work Package | Total Scope | Delivered | Installed | QC Accepted | Crews Mobilised | IFC Status |",
            "|---|---|---|---|---|---|---|",
            f"| Piling (`WP-CON-CIV-PIL`) | 15,400 piles | {new_state['work_packages']['WP-CON-CIV-PIL']['delivered']:,.0f} | {new_state['work_packages']['WP-CON-CIV-PIL']['installed']:,.0f} | {new_state['work_packages']['WP-CON-CIV-PIL']['qc_accepted']:,.0f} | {new_state['work_packages']['WP-CON-CIV-PIL']['crews_mobilised']} rigs | {'Released' if new_state['work_packages']['WP-CON-CIV-PIL']['ifc_released'] else 'Not Released'} |",
            f"| Trackers (`WP-CON-MEC-TRK`) | 5,100 tables | {new_state['work_packages']['WP-CON-MEC-TRK']['delivered']:,.0f} | {new_state['work_packages']['WP-CON-MEC-TRK']['installed']:,.0f} | {new_state['work_packages']['WP-CON-MEC-TRK']['qc_accepted']:,.0f} | {new_state['work_packages']['WP-CON-MEC-TRK']['crews_mobilised']} crews | {'Released' if new_state['work_packages']['WP-CON-MEC-TRK']['ifc_released'] else 'Not Released'} |",
            f"| Modules (`WP-CON-MEC-MOD`) | 172,800 units | {new_state['work_packages']['WP-CON-MEC-MOD']['delivered']:,.0f} | {new_state['work_packages']['WP-CON-MEC-MOD']['installed']:,.0f} | {new_state['work_packages']['WP-CON-MEC-MOD']['qc_accepted']:,.0f} | {new_state['work_packages']['WP-CON-MEC-MOD']['crews_mobilised']} crews | {'Released' if new_state['work_packages']['WP-CON-MEC-MOD']['ifc_released'] else 'Not Released'} |",
            f"| Mobilization (`WP-CON-MOB`) | 100.0 % | 100.0 % | {new_state['work_packages']['WP-CON-MOB']['installed']:.1f} % | {new_state['work_packages']['WP-CON-MOB']['qc_accepted']:.1f} % | {new_state['work_packages']['WP-CON-MOB']['crews_mobilised']} crews | Released |",
            ""
        ]
        with open(brief_md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines) + "\n")

    res_summary = {
        "day": target_day,
        "piles": int(new_state["work_packages"]["WP-CON-CIV-PIL"]["installed"]),
        "modules": int(new_state["work_packages"]["WP-CON-MEC-MOD"]["installed"]),
        "spi": evm_metrics["spi"],
        "cpi": evm_metrics["cpi"],
        "active_events": [e["event_id"] for e in active_events]
    }
    return res_summary, new_state

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run simulation day state transition")
    parser.add_argument("--day", type=int, help="Single target day to compute")
    parser.add_argument("--from", dest="from_day", type=int, help="Starting day of range")
    parser.add_argument("--to", dest="to_day", type=int, help="Ending day of range")
    parser.add_argument("--dry-run", action="store_true", help="Execute without updating live project_state.json")
    args = parser.parse_args()

    if args.day:
        res, _ = run_simulation_day(args.day, write_state=not args.dry_run)
        print(json.dumps(res, indent=2))
    elif args.from_day and args.to_day:
        state_acc = None
        hist_acc = []
        for d in range(args.from_day, args.to_day + 1):
            res, state_acc = run_simulation_day(d, prior_state=state_acc, history=hist_acc, write_state=not args.dry_run)
            hist_acc.append({
                "day": d,
                "bcwp": state_acc["project_totals"]["bcwp_usd"],
                "spi": res["spi"],
                "cpi": res["cpi"]
            })
            evts = ",".join(res["active_events"]) if res["active_events"] else "none"
            print(f"Day {res['day']:3d} | Piles: {res['piles']:5d} | Modules: {res['modules']:6d} | SPI: {res['spi']:.4f} | CPI: {res['cpi']:.4f} | Events: {evts}")
    else:
        print("Usage: python3 engine/run_day.py --day N OR python3 engine/run_day.py --from START --to END")
