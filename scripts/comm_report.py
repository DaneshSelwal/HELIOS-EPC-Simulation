#!/usr/bin/env python3
"""
Communication Report Generator for HELIOS EPC Simulation.
Reads 11_Shared_Registers/Communication_Log.csv and generates
11_Shared_Registers/COMM_MATRIX.md
"""

import os
import csv
import json
from collections import defaultdict

LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "11_Shared_Registers", "Communication_Log.csv")
REPORT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "11_Shared_Registers", "COMM_MATRIX.md")
IDENTITIES_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts", "agent_identities.json")

DEPTS = ["PMO", "PLN", "ENG", "SCM", "CON", "QAQ", "EHS", "COM", "TNC", "ADM", "SUB", "EXT"]

def load_data():
    if not os.path.exists(LOG_PATH):
        return []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def load_agents():
    if not os.path.exists(IDENTITIES_PATH):
        return {}
    with open(IDENTITIES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_report():
    rows = load_data()
    known_agents = load_agents()

    # a) from-dept x to-dept matrix
    matrix = {f: {t: 0 for t in DEPTS} for f in DEPTS}
    for r in rows:
        f_d = r.get("from_dept", "PMO")
        t_d = r.get("to_dept", "PMO")
        if f_d not in matrix:
            matrix[f_d] = {t: 0 for t in DEPTS}
        if t_d not in matrix[f_d]:
            matrix[f_d][t_d] = 0
        matrix[f_d][t_d] += 1

    # b) sent/received per agent
    sent_counts = defaultdict(int)
    recv_counts = defaultdict(int)
    for r in rows:
        f_a = r.get("from_agent", "UNSPECIFIED").upper()
        t_a = r.get("to_agent", "UNSPECIFIED").upper()
        sent_counts[f_a] += 1
        recv_counts[t_a] += 1

    # c) agents with ZERO messages
    all_agent_names = set(known_agents.keys())
    all_agent_names.add("PATRON")
    all_agent_names.add("DANESH")
    zero_sent = sorted([a for a in all_agent_names if sent_counts[a] == 0])
    zero_both = sorted([a for a in all_agent_names if sent_counts[a] == 0 and recv_counts[a] == 0])

    # d) open items past their action-by day
    current_day = max([int(r["sim_day"]) for r in rows if r["sim_day"].isdigit()] or [79])
    open_items = [r for r in rows if r.get("status") == "open"]

    # e) last 20 messages
    last_20 = rows[-20:] if len(rows) >= 20 else rows

    # Build Markdown
    lines = []
    lines.append("# HELIOS EPC Communication Matrix & Analysis Report")
    lines.append(f"**Total Messages Tracked**: {len(rows)}  ")
    lines.append(f"**Current Simulation Clock**: Day {current_day}  \n")
    lines.append("---")

    # Section a) Matrix
    lines.append("\n## a) Department Communication Matrix (FROM \\ TO)")
    header = "| FROM \\ TO | " + " | ".join(DEPTS) + " | Total Sent |"
    sep = "|---|" + "|".join(["---"] * len(DEPTS)) + "|---|"
    lines.append(header)
    lines.append(sep)

    col_totals = {t: 0 for t in DEPTS}
    grand_total = 0

    for f_d in DEPTS:
        row_str = f"| **{f_d}** |"
        row_sum = 0
        for t_d in DEPTS:
            val = matrix.get(f_d, {}).get(t_d, 0)
            row_str += f" {val} |"
            row_sum += val
            col_totals[t_d] += val
        row_str += f" **{row_sum}** |"
        grand_total += row_sum
        lines.append(row_str)

    # Total Recv row
    tot_row = "| **Total Recv** |"
    for t_d in DEPTS:
        tot_row += f" **{col_totals[t_d]}** |"
    tot_row += f" **{grand_total}** |"
    lines.append(tot_row)

    # Section b) Agent Sent/Received
    lines.append("\n---")
    lines.append("\n## b) Message Volume Per Agent")
    lines.append("| Agent Codename | Role Description | Sent Count | Received Count | Total Involvements |")
    lines.append("|---|---|---|---|---|")

    sorted_agents = sorted(all_agent_names, key=lambda a: (sent_counts[a] + recv_counts[a]), reverse=True)
    for a in sorted_agents:
        role = known_agents.get(a, {}).get("name", a)
        s = sent_counts[a]
        r = recv_counts[a]
        lines.append(f"| **{a}** | {role} | {s} | {r} | {s + r} |")

    # Section c) Agents with Zero Messages
    lines.append("\n---")
    lines.append("\n## c) Agents with ZERO Messages Sent")
    if zero_sent:
        lines.append(f"Total Agents with Zero Messages Sent: **{len(zero_sent)}** / {len(all_agent_names)}\n")
        lines.append("| Agent | Role | Status |")
        lines.append("|---|---|---|")
        for a in zero_sent:
            role = known_agents.get(a, {}).get("name", a)
            is_both = "Zero Sent & Zero Recv" if a in zero_both else "Received only"
            lines.append(f"| {a} | {role} | {is_both} |")
    else:
        lines.append("None. All agents have sent at least one message.")

    # Section d) Open Items Past Action-By Day
    lines.append("\n---")
    lines.append("\n## d) Open Items Past Action-By Day")
    if open_items:
        lines.append(f"Open Items Found: **{len(open_items)}**\n")
        lines.append("| Msg-ID | Sim Day | From -> To | Type | Priority | Topic | Issue | Status |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for it in open_items:
            lines.append(f"| {it['msg_id']} | Day {it['sim_day']} | {it['from_agent']} -> {it['to_agent']} | {it['type']} | {it['priority']} | {it['topic'][:50]} | #{it['issue_no']} | {it['status']} |")
    else:
        lines.append("All tracked items are currently answered or closed. No open items pending action.")

    # Section e) Last 20 Messages
    lines.append("\n---")
    lines.append("\n## e) Last 20 Messages (Chronological by Real Timestamp)")
    lines.append("| Msg-ID | Real Timestamp (UTC) | Sim Day | From -> To | Type | Priority | Topic | Link |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for m in reversed(last_20):
        url = m.get("comment_url", "")
        link = f"[Comment]({url})" if url else "N/A"
        lines.append(f"| `{m['msg_id']}` | {m['real_timestamp']} | Day {m['sim_day']} | {m['from_agent']} -> {m['to_agent']} | {m['type']} | {m['priority']} | {m['topic'][:45]} | {link} |")

    content = "\n".join(lines) + "\n"
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Generated {REPORT_PATH} successfully ({len(lines)} lines).")
    return content

if __name__ == "__main__":
    generate_report()
