#!/usr/bin/env python3
"""
HELIOS EPC Coded Message Posting, GitHub Channel Router & .md Folder Archiver.
Assigns Coded Mail ID:
  HEL-D{DDD}-{FROM_DEPT}-{TO_DEPT}-{WORK_CODE}-{TYPE}-{NNNN}
Routes every message to one of the 10 structured GitHub Issue Channels (CH-01 to CH-10),
appends to 11_Shared_Registers/Communication_Log.csv, auto-marks parent messages as 'answered',
and writes aligned Markdown (.md) files into:
  1. 11_Shared_Registers/Communications_Archive/Day_NNN/{MSG_ID}_{FROM}_to_{TO}.md
  2. 11_Shared_Registers/Communications_Archive/Day_NNN/DAILY_MAIL_DIGEST_Day{NNN}.md
  3. Departmental Mailboxes: <Dept_Folder>/Communications_<DEPT>.md
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

from scripts.comm_log import AGENT_DEPT, COLUMNS, DEPTS, TYPES, PRIORITIES, STATUSES, update_status

COMM_LOG_PATH = os.path.join(REPO_ROOT, "11_Shared_Registers", "Communication_Log.csv")
THREAD_TRACKER_PATH = os.path.join(REPO_ROOT, "state", "thread_issues.json")
ARCHIVE_ROOT = os.path.join(REPO_ROOT, "11_Shared_Registers", "Communications_Archive")

DEPT_FOLDER_MAP = {
    "PMO": "00_Project_Overview/Communications_PMO.md",
    "PLN": "01_Planning_Controls/Communications_PLN.md",
    "ENG": "02_Engineering_Design/Communications_ENG.md",
    "SCM": "03_SCM/Communications_SCM.md",
    "CON": "04_Construction/Communications_CON.md",
    "QAQ": "05_Quality/Communications_QAQ.md",
    "EHS": "06_EHS/Communications_EHS.md",
    "COM": "07_Contracts/Communications_COM.md",
    "TNC": "08_TC/Communications_TNC.md",
    "ADM": "09_Admin/Communications_ADM.md",
    "SUB": "10_Subcontractors/Communications_SUB.md",
    "EXT": "16_External_Parties/Communications_EXT.md",
}

CHANNEL_ROUTING = {
    "PD": ("CH-01", 11),
    "PMO": ("CH-02", 12),
    "PLN": ("CH-02", 12),
    "ENG": ("CH-03", 13),
    "SCM": ("CH-04", 14),
    "CON_CIV": ("CH-05", 15),
    "CON_ELE": ("CH-06", 16),
    "QAQ": ("CH-07", 17),
    "EHS": ("CH-08", 18),
    "ADM": ("CH-08", 18),
    "COM": ("CH-09", 19),
    "TNC": ("CH-10", 20),
}

def infer_work_code(subject, body, from_agent, to_agent):
    text = f"{subject} {body}".upper()
    if any(k in text for k in ["MPT", "TRANSFORMER", "WP-PROC-TRA", "POWERTRANS", "5.2G", "SFRA"]):
        return "TRA"
    if any(k in text for k in ["GIS", "SWITCHGEAR", "WP-PROC-GIS"]):
        return "GIS"
    if any(k in text for k in ["PILE", "PILING", "ROCK", "BLOCK 6", "FDC-CIV-001", "WP-CON-CIV-PIL"]):
        return "PIL"
    if any(k in text for k in ["TRACKER", "MMS", "TORQUE TUBE", "WP-CON-MEC-TRK", "SOLARIS"]):
        return "TRK"
    if any(k in text for k in ["MODULE", "TOPCON", "LUMINOS", "MICROCRACK", "WP-CON-MEC-MOD", "WP-PROC-MOD"]):
        return "MOD"
    if any(k in text for k in ["INVERTER", "PCS", "PPC", "INVERSA", "WP-PROC-INV"]):
        return "INV"
    if any(k in text for k in ["CABLE", "VLF", "TRENCH", "DC", "MV", "WP-CON-ELE"]):
        return "CAB"
    if any(k in text for k in ["FOUNDATION", "PLINTH", "CONCRETE", "CUBE", "WP-CON-CIV-FND"]):
        return "FND"
    if any(k in text for k in ["SUBSTATION", "220KV", "GSS", "PROTECTION", "PFR", "GRID", "WP-ENG-SUB"]):
        return "SUB"
    if any(k in text for k in ["COMMISSION", "PR TEST", "PAC", "IV CURVE", "WP-TNC"]):
        return "TNC"
    if any(k in text for k in ["GRADING", "CLEARING", "ROAD", "WP-CON-CIV-GRD"]):
        return "CIV"
    if any(k in text for k in ["MOBILIZATION", "LNTP", "KICKOFF", "CAMP", "WP-CON-MOB"]):
        return "MOB"
    return "GEN"

def resolve_channel(from_agent, to_agent, from_dept, to_dept, subject, work_code):
    if to_agent.upper() in ["PD", "DANESH"] or from_agent.upper() in ["PD", "DANESH"] or "[PD BRIEF]" in subject.upper():
        return "CH-01", 11
    if from_dept == "COM" or to_dept == "COM":
        return "CH-09", 19
    if from_dept == "QAQ" or to_dept == "QAQ":
        return "CH-07", 17
    if from_dept in ["EHS", "ADM"] or to_dept in ["EHS", "ADM"]:
        return "CH-08", 18
    if from_dept == "TNC" or to_dept == "TNC" or to_agent.upper() == "GRIDMASTER":
        return "CH-10", 20
    if from_dept == "SCM" or to_dept == "SCM":
        return "CH-04", 14
    if from_dept == "ENG" or to_dept == "ENG":
        return "CH-03", 13
    if from_dept in ["CON", "SUB"] or to_dept in ["CON", "SUB"]:
        if work_code in ["CAB", "INV", "FND", "SUB"]:
            return "CH-06", 16
        return "CH-05", 15
    return "CH-02", 12

def get_next_msg_num():
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
    return res.stdout.strip(), res.returncode

def append_to_dept_markdown(dept_code, row_data, formatted_block):
    rel_md = DEPT_FOLDER_MAP.get(dept_code, "00_Project_Overview/Communications_PMO.md")
    full_md = os.path.join(REPO_ROOT, rel_md)
    os.makedirs(os.path.dirname(full_md), exist_ok=True)

    if not os.path.exists(full_md):
        header = [
            f"# HELIOS EPC — Department `{dept_code}` Coded Communications Log",
            "",
            f"**Department Code**: `{dept_code}`  ",
            "**Mail Coding Format**: `HEL-D{DDD}-{FROM_DEPT}-{TO_DEPT}-{WORK_CODE}-{TYPE}-{NNNN}`  ",
            "",
            "## 1. Department Mail Index Table",
            "",
            "| Mail Code (Msg-ID) | Sim Day | Channel | From -> To (CC) | Work Code | Type | Priority | Subject | Status |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
            "",
            "## 2. Full Coded Mail Records",
            ""
        ]
        with open(full_md, "w", encoding="utf-8") as f:
            f.write("\n".join(header))

    with open(full_md, "r", encoding="utf-8") as f:
        content = f.read()

    index_row = (
        f"| `{row_data['msg_id']}` | Day {int(row_data['sim_day']):03d} | `{row_data['channel']}` (#{row_data['issue_no']}) | "
        f"**{row_data['from_agent']}** -> **{row_data['to_agent']}** ({row_data['cc']}) | `{row_data['work_code']}` | "
        f"`{row_data['type']}` | `{row_data['priority'].upper()}` | {row_data['topic']} | `{row_data['status'].upper()}` |"
    )

    if "## 2. Full Coded Mail Records" in content:
        parts = content.split("## 2. Full Coded Mail Records", 1)
        new_content = (
            parts[0].rstrip() + "\n" + index_row + "\n\n## 2. Full Coded Mail Records\n" +
            parts[1].rstrip() + "\n\n" + formatted_block + "\n"
        )
    else:
        new_content = content.rstrip() + "\n\n" + index_row + "\n\n" + formatted_block + "\n"

    with open(full_md, "w", encoding="utf-8") as f:
        f.write(new_content)
    return rel_md

def write_archive_markdown(row_data, formatted_block):
    sim_day = int(row_data["sim_day"])
    day_dir = os.path.join(ARCHIVE_ROOT, f"Day_{sim_day:03d}")
    os.makedirs(day_dir, exist_ok=True)

    # 1. Individual message .md file
    indiv_name = f"{row_data['msg_id']}_{row_data['from_agent']}_to_{row_data['to_agent']}.md"
    indiv_path = os.path.join(day_dir, indiv_name)
    with open(indiv_path, "w", encoding="utf-8") as f:
        f.write(formatted_block + "\n")

    # 2. Daily digest .md file
    digest_path = os.path.join(day_dir, f"DAILY_MAIL_DIGEST_Day{sim_day:03d}.md")
    if not os.path.exists(digest_path):
        with open(digest_path, "w", encoding="utf-8") as f:
            f.write(f"# HELIOS EPC — Daily Coded Communications Digest (Day {sim_day:03d})\n\n")
    with open(digest_path, "a", encoding="utf-8") as f:
        f.write(formatted_block + "\n\n")

    return os.path.relpath(indiv_path, REPO_ROOT), os.path.relpath(digest_path, REPO_ROOT)

def post_message(from_agent, to_agent, msg_type, priority, subject, body, sim_day, sim_time="09:00",
                 action_by_day=None, parent_msg_id="", cc_agents=None, work_code=None, dry_run=False):
    from_dept = AGENT_DEPT.get(from_agent.upper(), "PMO")
    to_dept = AGENT_DEPT.get(to_agent.upper(), "PMO")
    msg_type = msg_type.upper() if msg_type.upper() in TYPES else "INF"
    priority = priority.lower() if priority.lower() in PRIORITIES else "med"

    w_code = (work_code or infer_work_code(subject, body, from_agent, to_agent)).upper()
    ch_code, issue_no = resolve_channel(from_agent, to_agent, from_dept, to_dept, subject, w_code)

    next_num = get_next_msg_num()
    msg_id = f"HEL-D{int(sim_day):03d}-{from_dept}-{to_dept}-{w_code}-{msg_type}-{next_num:04d}"
    real_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    action_by_str = f"Day {int(action_by_day):03d}" if (action_by_day is not None and str(action_by_day).isdigit()) else f"Day {int(sim_day)+1:03d}"
    cc_str = ", ".join(cc_agents) if isinstance(cc_agents, list) and cc_agents else (str(cc_agents) if cc_agents else "None")
    parent_ref = parent_msg_id if parent_msg_id else "None"

    # Build Structured Coded Mail Block
    md_block = "\n".join([
        f"### Mail Record: `{msg_id}` — {subject}",
        "",
        "| Mail Field | Coded Value |",
        "| :--- | :--- |",
        f"| **Mail Code (Msg-ID)** | `{msg_id}` |",
        f"| **Channel & Issue** | `{ch_code}` (GitHub Issue `#{issue_no}`) |",
        f"| **From -> To (CC)** | **{from_agent.upper()}** (`{from_dept}`) -> **{to_agent.upper()}** (`{to_dept}`) \\| CC: `{cc_str}` |",
        f"| **Work Package Code** | `{w_code}` |",
        f"| **Type & Priority** | `{msg_type}` \\| Priority: `{priority.upper()}` \\| Action By: `{action_by_str}` |",
        f"| **Sim Timestamp** | Sim Day `{int(sim_day):03d}` `{sim_time}` \\| Real UTC: `{real_iso}` |",
        f"| **Parent Reference** | `{parent_ref}` |",
        "",
        body.strip()
    ])

    comment_url = f"https://github.com/DaneshSelwal/HELIOS-EPC-Simulation/issues/{issue_no}#issuecomment-{next_num:04d}"
    if not dry_run and os.environ.get("HELIOS_OFFLINE", "0") != "1":
        cmd = f"gh issue comment {issue_no} --body {json.dumps(md_block)}"
        out, rc = run_command(cmd)
        if rc == 0 and out.startswith("http"):
            comment_url = out

    # Auto-close parent message in Communication_Log.csv when replied to
    if parent_ref and parent_ref != "None":
        update_status(parent_ref, "answered")

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
        "topic": f"[{ch_code}|{w_code}] {subject}",
        "priority": priority,
        "issue_no": str(issue_no),
        "comment_url": comment_url,
        "parent_msg_id": parent_ref,
        "status": "open",
        "channel": ch_code,
        "work_code": w_code
    }

    csv_row = {k: row_data[k] for k in COLUMNS}
    file_exists = os.path.exists(COMM_LOG_PATH)
    with open(COMM_LOG_PATH, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        if not file_exists or os.path.getsize(COMM_LOG_PATH) == 0:
            writer.writeheader()
        writer.writerow(csv_row)

    # Write .md files to Central Archive & Departmental Folders
    indiv_rel, digest_rel = write_archive_markdown(row_data, md_block)
    from_md_rel = append_to_dept_markdown(from_dept, row_data, md_block)
    to_md_rel = append_to_dept_markdown(to_dept, row_data, md_block) if to_dept != from_dept else from_md_rel

    return {
        "msg_id": msg_id,
        "channel": ch_code,
        "work_code": w_code,
        "issue_no": issue_no,
        "comment_url": comment_url,
        "archive_md": indiv_rel,
        "dept_mds": sorted(list({from_md_rel, to_md_rel}))
    }

if __name__ == "__main__":
    print("Upgraded post_messages module loaded.")
