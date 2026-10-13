#!/usr/bin/env python3
"""
HELIOS EPC Message Posting & GitHub Integration Script.
Assigns Msg-ID: HEL-{FROMDEPT}-{TODEPT}-{TYPE}-{NNNN}
Builds coded header:
  **[{AGENT}]** -> {TO} | cc: {CC}
  Msg-ID: {MSG-ID} | Re: {PARENT} | Sim: Day {D} {TIME} | Real: {ISO} | Type: {T} | Priority: {P} | Action by: Day {D}
Posts:
  - Issue #11 for ATLAS PD briefs only.
  - One issue per topic thread for others.
Appends row to 11_Shared_Registers/Communication_Log.csv.
Applies GitHub labels.
Commits via scripts/agent_commit.py.
Python Standard Library only.
"""

import csv
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

from scripts.comm_log import AGENT_DEPT, COLUMNS, DEPTS, TYPES, PRIORITIES, STATUSES

COMM_LOG_PATH = os.path.join(REPO_ROOT, "11_Shared_Registers", "Communication_Log.csv")
THREAD_TRACKER_PATH = os.path.join(REPO_ROOT, "state", "thread_issues.json")

def get_next_msg_num():
    """Finds next sequential 4-digit number from Communication_Log.csv"""
    max_num = 0
    if os.path.exists(COMM_LOG_PATH):
        with open(COMM_LOG_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                msg_id = row.get("msg_id", "")
                m = re.search(r"-(\d{4})$", msg_id)
                if m:
                    num = int(m.group(1))
                    if num > max_num:
                        max_num = num
    return max_num + 1

def run_command(cmd):
    res = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if res.returncode != 0:
        print(f"Command failed ({res.returncode}): {cmd}\nStderr: {res.stderr}", file=sys.stderr)
    return res.stdout.strip(), res.returncode

def ensure_label_exists(label_name):
    cmd = f'gh label list --json name -q ".[].name"'
    out, rc = run_command(cmd)
    existing_labels = set(out.splitlines())
    if label_name not in existing_labels:
        # Create label
        run_command(f'gh label create "{label_name}" --color "ededed" --force')

def post_message(from_agent, to_agent, msg_type, priority, subject, body, sim_day, sim_time="09:00", action_by_day=None, parent_msg_id="", cc_agents=None, thread_key=None):
    """
    Constructs message, posts to GitHub, logs in Communication_Log.csv, and commits.
    """
    from_dept = AGENT_DEPT.get(from_agent.upper(), "ENG")
    to_dept = AGENT_DEPT.get(to_agent.upper(), "ENG")
    msg_type = msg_type.upper()
    if msg_type not in TYPES:
        msg_type = "INF"
    priority = priority.lower()
    if priority not in PRIORITIES:
        priority = "med"

    next_num = get_next_msg_num()
    msg_id = f"HEL-{from_dept}-{to_dept}-{msg_type}-{next_num:04d}"
    real_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    action_by_str = f"Day {action_by_day:03d}" if action_by_day else f"Day {sim_day+1:03d}"
    cc_str = ", ".join(cc_agents) if cc_agents else "None"
    parent_ref = parent_msg_id if parent_msg_id else "None"

    # Format Coded Header
    header_lines = [
        f"**[{from_agent.upper()}]** -> {to_agent.upper()} | cc: {cc_str}",
        f"Msg-ID: {msg_id} | Re: {parent_ref} | Sim: Day {sim_day:03d} {sim_time} | Real: {real_iso} | Type: {msg_type} | Priority: {priority} | Action by: {action_by_str}",
        "",
        body
    ]
    formatted_body = "\n".join(header_lines)

    # Load thread tracker
    os.makedirs(os.path.dirname(THREAD_TRACKER_PATH), exist_ok=True)
    threads = {}
    if os.path.exists(THREAD_TRACKER_PATH):
        with open(THREAD_TRACKER_PATH, "r", encoding="utf-8") as f:
            threads = json.load(f)

    issue_no = None
    comment_url = ""

    # Rule 1: Issue #11 is for ATLAS PD briefs only
    is_pd_brief = (to_agent.upper() in ["PD", "DANESH"]) or ("[PD BRIEF]" in subject.upper()) or (from_agent.upper() == "ATLAS" and to_agent.upper() == "PD")

    if is_pd_brief:
        issue_no = 11
        cmd = f"gh issue comment 11 --body {json.dumps(formatted_body)}"
        out, rc = run_command(cmd)
        comment_url = out if out.startswith("http") else f"https://github.com/DaneshSelwal/HELIOS-EPC-Simulation/issues/11#issuecomment-{next_num}"
    else:
        # Check if existing thread issue exists
        effective_thread_key = thread_key or parent_msg_id or subject.split(":")[0].strip()
        if effective_thread_key in threads:
            issue_no = threads[effective_thread_key]
            cmd = f"gh issue comment {issue_no} --body {json.dumps(formatted_body)}"
            out, rc = run_command(cmd)
            comment_url = out if out.startswith("http") else f"https://github.com/DaneshSelwal/HELIOS-EPC-Simulation/issues/{issue_no}#issuecomment-{next_num}"
        else:
            # Create new topic issue
            issue_title = f"[{msg_id}] D{sim_day:03d} | {from_dept} -> {to_dept} | {subject}"
            labels = [
                f"from:{from_dept.lower()}",
                f"to:{to_dept.lower()}",
                f"type:{msg_type.lower()}",
                f"prio:{priority.lower()}",
                "status:open"
            ]
            for lbl in labels:
                ensure_label_exists(lbl)

            lbl_args = " ".join([f'--label "{lbl}"' for lbl in labels])
            cmd = f"gh issue create --title {json.dumps(issue_title)} --body {json.dumps(formatted_body)} {lbl_args}"
            out, rc = run_command(cmd)
            # out contains issue url e.g. https://github.com/DaneshSelwal/HELIOS-EPC-Simulation/issues/12
            comment_url = out
            m_iss = re.search(r'/issues/(\d+)', out)
            if m_iss:
                issue_no = int(m_iss.group(1))
            else:
                issue_no = 12

            threads[effective_thread_key] = issue_no
            with open(THREAD_TRACKER_PATH, "w", encoding="utf-8") as f:
                json.dump(threads, f, indent=2)

    # Append to Communication_Log.csv
    row_data = {
        "msg_id": msg_id,
        "real_timestamp": real_iso,
        "sim_day": str(sim_day),
        "sim_time": sim_time,
        "from_agent": from_agent.upper(),
        "from_dept": from_dept,
        "to_agent": to_agent.upper(),
        "to_dept": to_dept,
        "cc": cc_str,
        "type": msg_type,
        "topic": subject,
        "priority": priority,
        "issue_no": str(issue_no),
        "comment_url": comment_url,
        "parent_msg_id": parent_ref,
        "status": "open"
    }

    file_exists = os.path.exists(COMM_LOG_PATH)
    with open(COMM_LOG_PATH, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        if not file_exists or os.path.getsize(COMM_LOG_PATH) == 0:
            writer.writeheader()
        writer.writerow(row_data)

    print(f"Posted {msg_id} on Issue #{issue_no}: {comment_url}")

    # Commit via agent_commit.py
    commit_script = os.path.join(REPO_ROOT, "scripts", "agent_commit.py")
    if os.path.exists(commit_script):
        commit_cmd = f'python3 "{commit_script}" --agent "{from_agent.upper()}" --message "comm({msg_type.lower()}): log {msg_id} - {subject[:40]}" --file "11_Shared_Registers/Communication_Log.csv"'
        run_command(commit_cmd)

    return {
        "msg_id": msg_id,
        "issue_no": issue_no,
        "comment_url": comment_url,
        "from_agent": from_agent.upper(),
        "to_agent": to_agent.upper(),
        "topic": subject,
        "sim_day": sim_day,
        "real_timestamp": real_iso
    }

if __name__ == "__main__":
    print("post_messages module loaded.")
