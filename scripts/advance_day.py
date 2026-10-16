#!/usr/bin/env python3
"""
Simulation Clock Advancer with Gating for HELIOS EPC Simulation.
Enforces strict quality and communication gating before advancing the simulation day.
Max 1 sim day per execution.
"""

import os
import sys
import json
import csv
import re
import subprocess
from datetime import datetime, timedelta

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLOCK_PATH = os.path.join(REPO_ROOT, "scripts", "sim_clock.json")
COMM_LOG_PATH = os.path.join(REPO_ROOT, "11_Shared_Registers", "Communication_Log.csv")
DELAY_LOG_PATH = os.path.join(REPO_ROOT, "01_Planning_Controls", "Delay_Event_Log.md")
DPR_DIR = os.path.join(REPO_ROOT, "12_Daily_Reports", "DPR")

def load_clock():
    if not os.path.exists(CLOCK_PATH):
        raise FileNotFoundError(f"Clock file not found at {CLOCK_PATH}")
    with open(CLOCK_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_clock(clock_data):
    with open(CLOCK_PATH, "w", encoding="utf-8") as f:
        json.dump(clock_data, f, indent=2)

def check_gate_i(current_day):
    """(i) DPR committed, KRONOS delay log reviewed, ATLAS brief posted for the current day."""
    errors = []

    # Check DPR file
    dpr_filename = f"DPR_Day{current_day:03d}.md"
    dpr_path = os.path.join(DPR_DIR, dpr_filename)
    if not os.path.exists(dpr_path):
        errors.append(f"Gate (i) Failed: DPR file {dpr_path} does not exist.")
    else:
        # Check git commit for DPR
        res = subprocess.run(["git", "log", "-n", "1", "--pretty=format:%H", "--", dpr_path],
                             cwd=REPO_ROOT, capture_output=True, text=True)
        if not res.stdout.strip():
            errors.append(f"Gate (i) Failed: DPR file {dpr_filename} is not committed in git.")

    # Check KRONOS delay log
    if not os.path.exists(DELAY_LOG_PATH):
        errors.append(f"Gate (i) Failed: Delay log {DELAY_LOG_PATH} does not exist.")
    else:
        with open(DELAY_LOG_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        day_pattern = rf"Day\s*0*{current_day}\b"
        if not re.search(day_pattern, content):
            errors.append(f"Gate (i) Failed: Delay Event Log has no validation entry for Day {current_day}.")

    # Check ATLAS brief in Communication_Log.csv
    atlas_brief_found = False
    if os.path.exists(COMM_LOG_PATH):
        with open(COMM_LOG_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("sim_day") == str(current_day) and row.get("from_agent", "").upper() == "ATLAS":
                    atlas_brief_found = True
                    break
    if not atlas_brief_found:
        errors.append(f"Gate (i) Failed: ATLAS daily briefing not posted/logged for Day {current_day}.")

    return errors

def check_gate_ii(current_day):
    """(ii) Every comment that day has a Msg-ID and a log row."""
    errors = []
    if not os.path.exists(COMM_LOG_PATH):
        return [f"Gate (ii) Failed: Communication log {COMM_LOG_PATH} does not exist."]

    msg_id_pattern = re.compile(r"^HEL-(?:D\d{3}-)?[A-Z]{3}-[A-Z]{3}-(?:[A-Z0-9]{3}-)?[A-Z]{3}-\d{4}$")
    logged_day_rows = 0

    with open(COMM_LOG_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("sim_day") == str(current_day):
                logged_day_rows += 1
                msg_id = row.get("msg_id", "")
                if not msg_id or not msg_id_pattern.match(msg_id):
                    errors.append(f"Gate (ii) Failed: Row for Day {current_day} has invalid Msg-ID: '{msg_id}'.")

    if logged_day_rows == 0:
        errors.append(f"Gate (ii) Failed: No communication rows logged for Day {current_day}.")

    return errors

def check_gate_iii(current_day):
    """(iii) No HIGH/CRITICAL issue has gone unanswered for more than 1 sim day."""
    errors = []
    if not os.path.exists(COMM_LOG_PATH):
        return [f"Gate (iii) Failed: Communication log {COMM_LOG_PATH} does not exist."]

    with open(COMM_LOG_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prio = row.get("priority", "").lower()
            status = row.get("status", "").lower()
            s_day_str = row.get("sim_day", "")
            if prio in ["high", "critical"] and status == "open" and s_day_str.isdigit():
                msg_day = int(s_day_str)
                if (current_day - msg_day) > 1:
                    errors.append(
                        f"Gate (iii) Failed: Unanswered {prio.upper()} message {row.get('msg_id')} "
                        f"from Day {msg_day} (>{current_day - msg_day} days old): '{row.get('topic')}'"
                    )
    return errors

def advance_simulation_day(dry_run=False):
    clock = load_clock()
    current_day = clock.get("day", 1)

    print(f"=== Evaluating Gating Requirements for Advancing Beyond Day {current_day} ===")
    
    e1 = check_gate_i(current_day)
    e2 = check_gate_ii(current_day)
    e3 = check_gate_iii(current_day)

    all_errors = e1 + e2 + e3

    if all_errors:
        print("\n[REFUSAL TO ADVANCE] Gating requirements not met:")
        for err in all_errors:
            print(f"  ❌ {err}")
        print("\nPlease resolve all open items and verify logging before advancing.")
        return False

    print("\n✅ Gate (i) Passed: DPR committed, KRONOS delay log verified, ATLAS brief logged.")
    print("✅ Gate (ii) Passed: All communication rows verified with valid HEL Msg-IDs.")
    print("✅ Gate (iii) Passed: No overdue HIGH/CRITICAL open items.")

    new_day = current_day + 1
    new_month = ((new_day - 1) // 28) + 1
    new_week = ((new_day - 1) // 7) + 1
    new_week_day = ((new_day - 1) % 7) + 1

    current_date = datetime.strptime(clock.get("sim_date", "2026-10-01"), "%Y-%m-%d")
    new_date = current_date + timedelta(days=1)

    clock["day"] = new_day
    clock["month"] = new_month
    clock["week"] = new_week
    clock["week_day"] = new_week_day
    clock["sim_date"] = new_date.strftime("%Y-%m-%d")
    clock["last_advanced_real_ts"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    if dry_run:
        print(f"\n[DRY RUN] Simulation clock would advance to Day {new_day} ({clock['sim_date']}, M{new_month}/W{new_week}D{new_week_day}).")
        return True

    save_clock(clock)
    print(f"\n🚀 Simulation clock advanced successfully to Day {new_day} ({clock['sim_date']}, Month {new_month} / Week {new_week} Day {new_week_day}).")
    return True

if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    success = advance_simulation_day(dry_run=dry_run)
    sys.exit(0 if success else 1)
