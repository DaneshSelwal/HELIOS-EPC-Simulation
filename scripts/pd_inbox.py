#!/usr/bin/env python3
"""
HELIOS EPC PD Inbox Processor.
Reads new comments by Danesh on Issue #11 (PD BRIEF - Phase 1).
Supports commands:
  - "INJECT EVT-nnn" (Injects specific pre-planted event into sim)
  - "DECIDE <msg-id> APPROVE|REJECT" (Executive decision on open item)
Generates inbox items for relevant agents.
Python Standard Library only.
"""

import json
import os
import re
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_FILE = os.path.join(REPO_ROOT, "state", "pd_inbox_processed.json")

def get_issue_comments(issue_no=11):
    cmd = ["gh", "api", f"repos/DaneshSelwal/HELIOS-EPC-Simulation/issues/{issue_no}/comments"]
    res = subprocess.run(cmd, text=True, capture_output=True)
    if res.returncode != 0:
        return []
    try:
        return json.loads(res.stdout)
    except Exception:
        return []

def load_processed_ids():
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def save_processed_ids(processed_set):
    os.makedirs(os.path.dirname(PROCESSED_FILE), exist_ok=True)
    with open(PROCESSED_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(list(processed_set)), f, indent=2)

def check_pd_inbox():
    """
    Checks Issue #11 for new comments and extracts Danesh commands.
    Returns list of inbox action items.
    """
    comments = get_issue_comments(11)
    processed = load_processed_ids()
    new_inbox_items = []

    for c in comments:
        c_id = str(c.get("id"))
        if c_id in processed:
            continue

        body = c.get("body", "")
        user = c.get("user", {}).get("login", "")

        # Only process human/PD comments (ignore bot/self comments unless testing)
        # Note: In this repo, Danesh's GitHub login is DaneshSelwal
        # Check for INJECT command
        inject_m = re.findall(r'INJECT\s+(EVT-\d{3})', body, re.IGNORECASE)
        for evt_id in inject_m:
            new_inbox_items.append({
                "type": "DANESH_INJECTION",
                "command": f"INJECT {evt_id.upper()}",
                "event_id": evt_id.upper(),
                "agent": "ATLAS",
                "source_comment_id": c_id,
                "created_at": c.get("created_at")
            })

        # Check for DECIDE command
        decide_m = re.findall(r'DECIDE\s+(HEL-[A-Z0-9\-]+)\s+(APPROVE|REJECT)', body, re.IGNORECASE)
        for msg_id, decision in decide_m:
            new_inbox_items.append({
                "type": "DANESH_DECISION",
                "command": f"DECIDE {msg_id} {decision.upper()}",
                "msg_id": msg_id,
                "decision": decision.upper(),
                "agent": "ATLAS",
                "source_comment_id": c_id,
                "created_at": c.get("created_at")
            })

        processed.add(c_id)

    save_processed_ids(processed)
    return new_inbox_items

if __name__ == "__main__":
    items = check_pd_inbox()
    print(f"Checked Issue #11. Found {len(items)} new PD commands.")
    for it in items:
        print(f"  - {it['command']} for {it['agent']}")
