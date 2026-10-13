#!/usr/bin/env python3
"""
Communication Log Manager for HELIOS EPC Simulation.
Manages 11_Shared_Registers/Communication_Log.csv
Supports appending messages, updating status, and backfilling from GitHub Issues #1-#10.
"""

import os
import sys
import csv
import json
import re
import argparse
import subprocess
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "11_Shared_Registers", "Communication_Log.csv")

DEPTS = ["PMO", "PLN", "ENG", "SCM", "CON", "QAQ", "EHS", "COM", "TNC", "ADM", "SUB", "EXT"]
TYPES = ["INS", "RFI", "NCR", "DEL", "NTC", "VO", "BIL", "RPT", "ESC", "EVT", "MOM", "INF"]
PRIORITIES = ["low", "med", "high", "critical"]
STATUSES = ["open", "answered", "closed"]

COLUMNS = [
    "msg_id",
    "real_timestamp",
    "sim_day",
    "sim_time",
    "from_agent",
    "from_dept",
    "to_agent",
    "to_dept",
    "cc",
    "type",
    "topic",
    "priority",
    "issue_no",
    "comment_url",
    "parent_msg_id",
    "status"
]

AGENT_DEPT = {
    # PMO
    "ATLAS": "PMO",
    "SIGMA": "PMO",
    # PLN
    "KRONOS": "PLN",
    "VECTOR": "PLN",
    "WATT": "PLN",
    # ENG
    "ARCHON": "ENG",
    "NEXGEN": "ENG",
    "CIPHER": "ENG",
    "TERRA": "ENG",
    "MERIDIAN": "ENG",
    "AMPERE": "ENG",
    "VOLTA": "ENG",
    "SOLARIS": "ENG",
    "RELAY": "ENG",
    # SCM
    "CONVOY": "SCM",
    "FORGE": "SCM",
    "VENDOR": "SCM",
    "TRACER": "SCM",
    "ROUTE": "SCM",
    "VAULT": "SCM",
    "DEPOT": "SCM",
    # CON
    "RAMPART": "CON",
    "BASTION": "CON",
    "SWITCHMAN": "CON",
    "ARCLINE": "CON",
    "FORTRESS": "CON",
    "CONDUIT": "CON",
    "STRATUM": "CON",
    "PRISM": "CON",
    # QAQ
    "SENTINEL": "QAQ",
    "PLUMBLINE": "QAQ",
    "OHMMETER": "QAQ",
    "TORQUE": "QAQ",
    "DOSSIER": "QAQ",
    # EHS
    "AEGIS": "EHS",
    "GUARDIAN": "EHS",
    "WARDEN": "EHS",
    "VERDANT": "EHS",
    # COM
    "COUNSEL": "COM",
    "CLAIMS": "COM",
    "INVOICE": "COM",
    "LEDGE": "COM",
    "CHECKER": "COM",
    "LEDGER": "COM",
    "LEDGER2": "COM",
    # TNC
    "IGNITE": "TNC",
    "SPARK": "TNC",
    "GRIDLOCK": "TNC",
    # ADM
    "SUMMIT": "ADM",
    "PERMIT": "ADM",
    # SUB
    "GROUNDWORK": "SUB",
    "EREKTOR": "SUB",
    "ELECTRA": "SUB",
    "GRIDCON": "SUB",
    # EXT (External stakeholders & NO_PERSONA_FILE entities)
    "PD": "EXT",
    "PATRON": "EXT",
    "AUDITOR": "EXT",
    "GRIDMASTER": "EXT",
    "LUMINOS": "EXT",
    "INVERSA": "EXT",
    "POWERTRANS": "EXT",
    "INSPECTOR": "EXT",
    "CERTIFIER": "EXT",
    "NEXUS": "EXT",
    "HERALD": "EXT",
    "NEGU": "EXT",
    "UZBEKENERGO": "EXT",
    "ALL": "PMO",
    "UNSPECIFIED": "PMO",
}

def ensure_csv_exists():
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(COLUMNS)

def get_next_msg_id(from_dept, to_dept, msg_type):
    ensure_csv_exists()
    count = 0
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for _ in reader:
            count += 1
    seq = count + 1
    return f"HEL-{from_dept}-{to_dept}-{msg_type}-{seq:04d}"

def append_row(row_dict):
    ensure_csv_exists()
    # Normalize fields
    from_dept = row_dict.get("from_dept") or AGENT_DEPT.get(row_dict.get("from_agent", "").upper(), "PMO")
    to_dept = row_dict.get("to_dept") or AGENT_DEPT.get(row_dict.get("to_agent", "").upper(), "PMO")
    msg_type = row_dict.get("type", "INF").upper()
    if msg_type not in TYPES:
        msg_type = "INF"
    
    msg_id = row_dict.get("msg_id")
    if not msg_id:
        msg_id = get_next_msg_id(from_dept, to_dept, msg_type)

    row = {
        "msg_id": msg_id,
        "real_timestamp": row_dict.get("real_timestamp") or datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "sim_day": str(row_dict.get("sim_day", "")),
        "sim_time": row_dict.get("sim_time", "08:00"),
        "from_agent": row_dict.get("from_agent", "UNSPECIFIED").upper(),
        "from_dept": from_dept,
        "to_agent": row_dict.get("to_agent", "UNSPECIFIED").upper(),
        "to_dept": to_dept,
        "cc": row_dict.get("cc", ""),
        "type": msg_type,
        "topic": (row_dict.get("topic", "")).replace("\n", " ").strip(),
        "priority": row_dict.get("priority", "med").lower(),
        "issue_no": str(row_dict.get("issue_no", "1")),
        "comment_url": row_dict.get("comment_url", ""),
        "parent_msg_id": row_dict.get("parent_msg_id", ""),
        "status": row_dict.get("status", "closed").lower()
    }

    with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writerow(row)
    return row

def update_status(msg_id, new_status):
    ensure_csv_exists()
    rows = []
    updated = False
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r["msg_id"] == msg_id:
                r["status"] = new_status.lower()
                updated = True
            rows.append(r)
    if updated:
        with open(LOG_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
    return updated

def parse_comment_text(body, title=""):
    """Heuristic extraction of sender, recipient, sim_day, topic, type, priority."""
    # From agent
    from_agent = "UNSPECIFIED"
    m_from = re.search(r'\*\*\[([A-Za-z0-9_-]+)\]\*\*', body)
    if m_from:
        cand = m_from.group(1).upper()
        if cand in AGENT_DEPT:
            from_agent = cand
    if from_agent == "UNSPECIFIED":
        m_from2 = re.search(r'(?:###|\*\*FROM_AGENT:\*\*)\s*([A-Za-z]+)', body)
        if m_from2 and m_from2.group(1).upper() in AGENT_DEPT:
            from_agent = m_from2.group(1).upper()
    if from_agent == "UNSPECIFIED":
        for a in AGENT_DEPT:
            if a in ["ALL", "UNSPECIFIED"]:
                continue
            if re.search(rf'\b{a}\b', body[:80].upper()):
                from_agent = a
                break

    from_dept = AGENT_DEPT.get(from_agent, "PMO")

    # To agent
    to_agent = "UNSPECIFIED"
    m_to = re.search(r'(?:\*\*TO:\*\*|To:|Attention:|\b->\s*)([^\n|]+)', body, re.IGNORECASE)
    if m_to:
        to_text = m_to.group(1).upper()
        if "DANESH" in to_text or "PROJECT DIRECTOR" in to_text:
            to_agent = "PD"
        elif "EMPLOYER" in to_text or "NEGU" in to_text or "PATRON" in to_text:
            to_agent = "PATRON"
        elif "ATLAS" in to_text:
            to_agent = "ATLAS"
        elif "KRONOS" in to_text:
            to_agent = "KRONOS"
        elif "RAMPART" in to_text:
            to_agent = "RAMPART"
        elif "SIGMA" in to_text:
            to_agent = "SIGMA"
        elif "ELECTRA" in to_text:
            to_agent = "ELECTRA"
        elif "ALL" in to_text or "DISCIPLINE" in to_text or "DEPARTMENT" in to_text:
            to_agent = "ALL"
        else:
            for a in AGENT_DEPT:
                if a in to_text and a not in ["ALL", "UNSPECIFIED"]:
                    to_agent = a
                    break

    # If still unspecified and sender is not ATLAS, default recipient to ATLAS
    if to_agent == "UNSPECIFIED":
        to_agent = "ATLAS" if from_agent != "ATLAS" else "PD"

    to_dept = AGENT_DEPT.get(to_agent, "PMO")

    # Sim day
    sim_day = ""
    m_day = re.search(r'\bDay\s*0*([1-9]\d?)\b', body, re.IGNORECASE)
    if not m_day:
        m_day = re.search(r'\bD0*([1-9]\d?)\b', body)
    if not m_day and title:
        m_day = re.search(r'\bDay\s*0*([1-9]\d?)\b', title, re.IGNORECASE)
    if m_day:
        sim_day = int(m_day.group(1))

    # Type
    msg_type = "INF"
    upper_body = body[:500].upper()
    if "DAILY PROGRESS REPORT" in upper_body or "DPR" in upper_body or "BRIEF" in upper_body or "TRANSMITTAL" in upper_body:
        msg_type = "RPT"
    elif "DIRECTIVE" in upper_body or "INSTRUCTION" in upper_body or "ORDER" in upper_body:
        msg_type = "INS"
    elif "NCR" in upper_body or "NON-CONFORMANCE" in upper_body:
        msg_type = "NCR"
    elif "RFI" in upper_body or "REQUEST FOR INFORMATION" in upper_body:
        msg_type = "RFI"
    elif "NOTICE" in upper_body or "CLAIM" in upper_body:
        msg_type = "NTC"
    elif "VARIATION" in upper_body or "VO" in upper_body:
        msg_type = "VO"
    elif "BILLING" in upper_body or "INVOICE" in upper_body:
        msg_type = "BIL"
    elif "DELAY" in upper_body or "SCHEDULE IMPACT" in upper_body:
        msg_type = "DEL"
    elif "EVENT" in upper_body or "EVT-" in upper_body:
        msg_type = "EVT"
    elif "STAND-UP" in upper_body or "MINUTES" in upper_body or "MOM" in upper_body:
        msg_type = "MOM"
    elif "ESCALATION" in upper_body or "URGENT" in upper_body:
        msg_type = "ESC"

    # Priority
    if msg_type in ["EVT", "ESC", "NCR"]:
        priority = "critical" if "EVT" in msg_type else "high"
    elif msg_type in ["RPT", "INS", "NTC", "DEL"]:
        priority = "high"
    else:
        priority = "med"

    # Topic
    topic = ""
    for line in body.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("#"):
            topic = re.sub(r'^[#\s*]+', '', line).strip()
            break
        if line.lower().startswith("subject:"):
            topic = line[8:].strip()
            break
    if not topic:
        topic = (body.splitlines()[0] if body.splitlines() else "Message").strip()
    topic = re.sub(r'[*_`#]', '', topic)[:100].strip()

    return {
        "from_agent": from_agent,
        "from_dept": from_dept,
        "to_agent": to_agent,
        "to_dept": to_dept,
        "sim_day": sim_day,
        "type": msg_type,
        "priority": priority,
        "topic": topic
    }

def backfill():
    repo = "DaneshSelwal/HELIOS-EPC-Simulation"
    print("Fetching comments for Issues #1 through #10...")
    all_comments = []
    for issue_no in range(1, 11):
        # Fetch issue metadata for title
        cmd_meta = ["gh", "issue", "view", str(issue_no), "--json", "title,body,createdAt,url"]
        res_meta = subprocess.run(cmd_meta, capture_output=True, text=True)
        issue_title = ""
        if res_meta.returncode == 0:
            meta = json.loads(res_meta.stdout)
            issue_title = meta.get("title", "")

        cmd = ["gh", "api", f"repos/{repo}/issues/{issue_no}/comments?per_page=100", "--paginate"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Error fetching comments for issue #{issue_no}: {res.stderr}")
            continue
        comments = json.loads(res.stdout)
        for c in comments:
            c["issue_no"] = issue_no
            c["issue_title"] = issue_title
            all_comments.append(c)

    # Sort comments chronologically by created_at
    all_comments.sort(key=lambda x: x["created_at"])
    print(f"Total comments fetched: {len(all_comments)}. Generating communication rows...")

    # Overwrite communication log with backfilled rows
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    rows = []
    seq = 1
    last_known_day = 1

    for c in all_comments:
        body = c.get("body", "")
        parsed = parse_comment_text(body, c.get("issue_title", ""))
        
        sim_day = parsed["sim_day"]
        if sim_day != "":
            last_known_day = sim_day
        else:
            sim_day = last_known_day

        from_dept = parsed["from_dept"]
        to_dept = parsed["to_dept"]
        msg_type = parsed["type"]
        msg_id = f"HEL-{from_dept}-{to_dept}-{msg_type}-{seq:04d}"
        seq += 1

        status = "closed"
        if msg_type in ["RFI", "NCR", "DEL"] and c["issue_no"] != 1:
            status = "answered"

        row = {
            "msg_id": msg_id,
            "real_timestamp": c["created_at"],
            "sim_day": str(sim_day),
            "sim_time": "08:00",
            "from_agent": parsed["from_agent"],
            "from_dept": from_dept,
            "to_agent": parsed["to_agent"],
            "to_dept": to_dept,
            "cc": "",
            "type": msg_type,
            "topic": parsed["topic"],
            "priority": parsed["priority"],
            "issue_no": str(c["issue_no"]),
            "comment_url": c["html_url"],
            "parent_msg_id": "",
            "status": status
        }
        rows.append(row)

    with open(LOG_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Successfully wrote {len(rows)} rows to {LOG_PATH}.")
    return len(rows)

def main():
    parser = argparse.ArgumentParser(description="HELIOS Communication Log Manager")
    subparsers = parser.add_subparsers(dest="subcommand")

    # append
    p_append = subparsers.add_parser("append", help="Append a new message row")
    p_append.add_argument("--from-agent", required=True)
    p_append.add_argument("--to-agent", default="UNSPECIFIED")
    p_append.add_argument("--type", default="INF", choices=TYPES)
    p_append.add_argument("--topic", required=True)
    p_append.add_argument("--priority", default="med", choices=PRIORITIES)
    p_append.add_argument("--sim-day", required=True)
    p_append.add_argument("--sim-time", default="08:00")
    p_append.add_argument("--issue-no", default="1")
    p_append.add_argument("--comment-url", default="")
    p_append.add_argument("--parent-msg-id", default="")
    p_append.add_argument("--status", default="closed", choices=STATUSES)
    p_append.add_argument("--cc", default="")

    # update
    p_update = subparsers.add_parser("update", help="Update message status")
    p_update.add_argument("--msg-id", required=True)
    p_update.add_argument("--status", required=True, choices=STATUSES)

    # backfill
    subparsers.add_parser("backfill", help="Backfill communication log from Issues #1-#10")

    args = parser.parse_args()

    if args.subcommand == "append":
        row = append_row(vars(args))
        print(f"Appended message: {row['msg_id']}")
    elif args.subcommand == "update":
        ok = update_status(args.msg_id, args.status)
        if ok:
            print(f"Updated {args.msg_id} status to {args.status}")
        else:
            print(f"Message ID {args.msg_id} not found.")
            sys.exit(1)
    elif args.subcommand == "backfill":
        backfill()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
