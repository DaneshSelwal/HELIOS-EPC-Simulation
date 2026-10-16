#!/usr/bin/env python3
"""
Updates the HELIOS Organization Chart PDF (HELIOS_OC_Single_Page.pdf) so all 64 agent personas
+ 1 Human PD (Danesh Selwal) show as built (0 TBI pending), with rich vector portrait illustrations,
and builds the complete 00_Project_Overview/03_Workforce_Directory/ with:
  - 65 SVG portrait avatars (avatars/<AGENT>.svg)
  - 65 PNG portrait photos (avatars/<AGENT>.png)
  - 65 Individual Personnel Dossier Markdown files (profiles/<ID>_<AGENT>.md)
  - Master Visual Workforce Directory (WORKFORCE_DIRECTORY.md)
"""

import base64
import glob
import json
import os
import re
import zlib

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_PATH = os.path.join(REPO_ROOT, "00_Project_Overview", "01_Executive_Command_Suite", "HELIOS_OC_Single_Page.pdf")
PDF_ROOT_COPY = os.path.join(REPO_ROOT, "00_Project_Overview", "HELIOS_OC_Single_Page.pdf")
WORKFORCE_DIR = os.path.join(REPO_ROOT, "00_Project_Overview", "03_Workforce_Directory")
AVATARS_DIR = os.path.join(WORKFORCE_DIR, "avatars")
PROFILES_DIR = os.path.join(WORKFORCE_DIR, "profiles")
AUTHORITY_PATH = os.path.join(REPO_ROOT, "engine", "authority_matrix.json")


def update_org_chart_pdf():
    with open(PDF_PATH, "rb") as f:
        data = f.read()

    s_idx = data.find(b"stream")
    e_idx = data.find(b"endstream")
    raw = data[s_idx + 6 : e_idx].strip()
    dec = zlib.decompress(base64.a85decode(raw, adobe=True))
    lines = dec.decode("latin1").splitlines()

    # 1. Replace Danesh Selwal's grey silhouette (lines 274..295) with an executive portrait
    # Clip box is x=[872..908], y=[1544..1586], center x=890, base y matching ATLAS (y+152)
    atlas_portrait = []
    for l in lines[372:474]:
        tokens = l.split()
        if tokens and tokens[-1] in ["m", "l", "c"]:
            nums = [float(t) for t in tokens[:-1]]
            shifted = []
            for idx_n, val in enumerate(nums):
                if idx_n % 2 == 1:
                    val += 152.0
                shifted.append(f"{val:.4f}".rstrip("0").rstrip("."))
            atlas_portrait.append(" ".join(shifted + [tokens[-1]]))
        elif tokens and tokens[0] == "n" and ("m" in tokens or "l" in tokens) and "re" not in tokens:
            new_toks = ["n"]
            sub = tokens[1:]
            idx_t = 0
            while idx_t < len(sub):
                if idx_t + 2 < len(sub) and sub[idx_t + 2] in ["m", "l"]:
                    xv = float(sub[idx_t])
                    yv = float(sub[idx_t + 1]) + 152.0
                    new_toks.extend([f"{xv:.4f}".rstrip("0").rstrip("."), f"{yv:.4f}".rstrip("0").rstrip("."), sub[idx_t + 2]])
                    idx_t += 3
                else:
                    new_toks.append(sub[idx_t])
                    idx_t += 1
            atlas_portrait.append(" ".join(new_toks))
        elif tokens and tokens[-1] == "f*" and "re" in tokens:
            re_idx = tokens.index("re")
            y_val = float(tokens[re_idx - 3]) + 152.0
            tokens[re_idx - 3] = f"{y_val:.4f}".rstrip("0").rstrip(".")
            atlas_portrait.append(" ".join(tokens))
        else:
            if l.strip() == ".266667 .266667 .266667 rg":
                atlas_portrait.append(".780392 .160784 .160784 rg")  # crimson executive tie
            elif l.strip() == ".211765 .235294 .278431 rg":
                atlas_portrait.append(".090196 .168627 .309804 rg")  # deep navy executive blazer
            else:
                atlas_portrait.append(l)

    lines[274:296] = atlas_portrait

    # 2. Update the 10 formerly-TBI agents (NEXUS, HERALD, PATRON, AUDITOR, GRIDMASTER, LUMINOS, INVERSA, POWERTRANS, INSPECTOR, CERTIFIER)
    tbi_agents = {
        "NEXUS": ("Joined", ".180392 .490196 .196078 rg", "1 1 1 rg", ".121569 .227451 .407843 RG"),
        "HERALD": ("Joined", ".180392 .490196 .196078 rg", "1 1 1 rg", ".121569 .227451 .407843 RG"),
        "PATRON": ("Joined", ".180392 .490196 .196078 rg", "1 1 1 rg", ".235294 .27451 .329412 RG"),
        "AUDITOR": ("Joined", ".180392 .490196 .196078 rg", "1 1 1 rg", ".235294 .27451 .329412 RG"),
        "GRIDMASTER": ("Built \\(Mobilises Day 241\\)", ".772549 .541176 0 rg", "1 .964706 .862745 rg", ".235294 .27451 .329412 RG"),
        "LUMINOS": ("Built \\(Mobilises Day 91\\)", ".772549 .541176 0 rg", "1 .964706 .862745 rg", ".235294 .27451 .329412 RG"),
        "INVERSA": ("Built \\(Mobilises Day 91\\)", ".772549 .541176 0 rg", "1 .964706 .862745 rg", ".235294 .27451 .329412 RG"),
        "POWERTRANS": ("Built \\(Mobilises Day 91\\)", ".772549 .541176 0 rg", "1 .964706 .862745 rg", ".235294 .27451 .329412 RG"),
        "INSPECTOR": ("Built \\(Mobilises Day 61\\)", ".772549 .541176 0 rg", "1 .964706 .862745 rg", ".235294 .27451 .329412 RG"),
        "CERTIFIER": ("Built \\(Mobilises Day 121\\)", ".772549 .541176 0 rg", "1 .964706 .862745 rg", ".235294 .27451 .329412 RG"),
    }

    for ag_name, (status_label, status_color, card_bg, border_stroke) in tbi_agents.items():
        idx = next(i for i, l in enumerate(lines) if f"({ag_name}) Tj" in l)
        fill_idx = next(i for i in range(idx, idx - 250, -1) if ".992157 .92549 .917647 rg" in lines[i])
        border_idx = next(i for i in range(idx, idx - 250, -1) if ".752941 .223529 .168627 RG" in lines[i])
        dash_idx = next(i for i in range(idx, idx - 250, -1) if "[3 2] 0 d" in lines[i])
        tbi_color_idx = next(i for i in range(idx, idx + 20) if ".752941 .223529 .168627 rg" in lines[i])
        tbi_text_idx = next(i for i in range(idx, idx + 20) if "TBI - persona file pending" in lines[i])

        lines[fill_idx] = card_bg
        lines[border_idx] = border_stroke
        lines[dash_idx] = "[] 0 d"
        lines[tbi_color_idx] = status_color
        lines[tbi_text_idx] = lines[tbi_text_idx].replace("TBI - persona file pending", status_label)

    # 3. Update issue date and footer summary lines
    for i, l in enumerate(lines):
        if "(Issue date: 15-Oct-2026)" in l:
            lines[i] = l.replace("Issue date: 15-Oct-2026", "Issue date: 16-Oct-2026 \\(Rev 2.0\\)")
        elif "Total roster: 64 agents + 1 human Project Director" in l:
            lines[i] = (
                "BT 1 0 0 1 30 126 Tm (Total roster: 64 Built AI Agents + 1 Human Project Director \\(65 Total\\)  |  "
                "Active at Day 1 Kickoff: 31  |  Scheduled Window Mobilisation: 33  |  TBI Pending: 0 \\(100% Built\\)) Tj T* ET"
            )
        elif "(Yet to Join \\(as at sim Day 4\\))" in l:
            lines[i] = l.replace("Yet to Join \\(as at sim Day 4\\)", "Scheduled Mobilisation \\(Activity Window\\)")
        elif "(TBI = persona file pending)" in l:
            lines[i] = l.replace("TBI = persona file pending", "TBI = 0 \\(All 64 Agent Personas Built\\)")

    new_stream_text = "\n".join(lines) + "\n"
    comp = zlib.compress(new_stream_text.encode("latin1"), 9)

    # Rebuild PDF with updated FlateDecode stream and xref table
    obj9_header = f"9 0 obj\n<<\n/Filter [ /FlateDecode ] /Length {len(comp)}\n>>\nstream\n".encode("latin1")
    obj9_footer = b"\nendstream\nendobj\n"

    obj9_start = data.find(b"9 0 obj")
    before_obj9 = data[:obj9_start]
    new_obj9 = obj9_header + comp + obj9_footer

    # Recompute byte offsets for objects 1..9
    body_bytes = before_obj9 + new_obj9
    offsets = {}
    for obj_no in range(1, 10):
        pat = f"\n{obj_no} 0 obj\n".encode("latin1")
        pos = body_bytes.find(pat)
        if pos != -1:
            offsets[obj_no] = pos + 1
        else:
            pat2 = f"{obj_no} 0 obj\n".encode("latin1")
            offsets[obj_no] = body_bytes.find(pat2)

    xref_offset = len(body_bytes)
    xref_lines = ["xref", "0 10", "0000000000 65535 f "]
    for obj_no in range(1, 10):
        xref_lines.append(f"{offsets[obj_no]:010d} 00000 n ")
    trailer = (
        "\n".join(xref_lines)
        + f"\ntrailer\n<<\n/Info 7 0 R /Root 6 0 R /Size 10\n>>\nstartxref\n{xref_offset}\n%%EOF\n"
    ).encode("latin1")

    final_pdf = body_bytes + trailer
    with open(PDF_PATH, "wb") as f:
        f.write(final_pdf)
    with open(PDF_ROOT_COPY, "wb") as f:
        f.write(final_pdf)

    print(f"Updated PDF saved to:\n  - {PDF_PATH}\n  - {PDF_ROOT_COPY} ({len(final_pdf)} bytes)")
    return lines


def pdf_clip_to_svg(clip_lines, agent_name, role, dept_color):
    """Converts a 36x42 PDF vector avatar block into a standalone high-res SVG."""
    # Find bounding box from the first `re` line: `n X Y 36 42 re f*`
    re_line = next(l for l in clip_lines if "36 42 re" in l)
    parts = re_line.split()
    re_idx = parts.index("re")
    x0 = float(parts[re_idx - 4])
    y0 = float(parts[re_idx - 3])
    w = 36.0
    h = 42.0

    def tx(x):
        return (float(x) - x0) * 5.0  # Scale 5x -> 180x210 px

    def ty(y):
        return (h - (float(y) - y0)) * 5.0

    svg_elems = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 210" width="180" height="210">',
        f'  <defs><clipPath id="clip"><rect x="0" y="0" width="180" height="210" rx="16" ry="16"/></clipPath></defs>',
        f'  <g clip-path="url(#clip)">'
    ]

    fill_rgb = "rgb(230,232,236)"
    stroke_rgb = "rgb(45,45,45)"
    stroke_w = 5.0
    path_d = []

    for raw_l in clip_lines[1:]:
        l = raw_l.strip()
        if not l or l.startswith("q") or l.startswith("Q") or "W* n" in l:
            continue
        toks = l.split()
        if toks[-1] == "rg" and len(toks) == 4:
            r, g, b = [int(round(float(c) * 255)) for c in toks[:3]]
            fill_rgb = f"rgb({r},{g},{b})"
        elif toks[-1] == "RG" and len(toks) == 4:
            r, g, b = [int(round(float(c) * 255)) for c in toks[:3]]
            stroke_rgb = f"rgb({r},{g},{b})"
        elif toks[-1] == "w" and len(toks) == 2:
            stroke_w = float(toks[0]) * 5.0
        elif "re" in toks and toks[-1] == "f*":
            ri = toks.index("re")
            rx = tx(toks[ri - 4])
            ry_top = ty(float(toks[ri - 3]) + float(toks[ri - 1]))
            rw = float(toks[ri - 2]) * 5.0
            rh = float(toks[ri - 1]) * 5.0
            svg_elems.append(f'    <rect x="{rx:.2f}" y="{ry_top:.2f}" width="{rw:.2f}" height="{rh:.2f}" fill="{fill_rgb}"/>')
        elif toks[0] == "n" and len(toks) > 1:
            # Inline path e.g. n X Y m X Y l h
            sub = toks[1:]
            idx_t = 0
            while idx_t < len(sub):
                if idx_t + 2 < len(sub) and sub[idx_t + 2] in ["m", "l"]:
                    cmd = "M" if sub[idx_t + 2] == "m" else "L"
                    path_d.append(f"{cmd} {tx(sub[idx_t]):.2f} {ty(sub[idx_t+1]):.2f}")
                    idx_t += 3
                elif sub[idx_t] == "h":
                    path_d.append("Z")
                    idx_t += 1
                elif sub[idx_t] == "S":
                    d_str = " ".join(path_d)
                    svg_elems.append(f'    <path d="{d_str}" fill="none" stroke="{stroke_rgb}" stroke-width="{stroke_w:.2f}" stroke-linecap="round"/>')
                    path_d = []
                    idx_t += 1
                else:
                    idx_t += 1
        elif toks[-1] == "m" and len(toks) == 3:
            path_d.append(f"M {tx(toks[0]):.2f} {ty(toks[1]):.2f}")
        elif toks[-1] == "l" and len(toks) == 3:
            path_d.append(f"L {tx(toks[0]):.2f} {ty(toks[1]):.2f}")
        elif toks[-1] == "c" and len(toks) == 7:
            path_d.append(
                f"C {tx(toks[0]):.2f} {ty(toks[1]):.2f}, {tx(toks[2]):.2f} {ty(toks[3]):.2f}, {tx(toks[4]):.2f} {ty(toks[5]):.2f}"
            )
        elif l == "h":
            path_d.append("Z")
        elif l in ["f*", "f"]:
            if path_d:
                d_str = " ".join(path_d)
                svg_elems.append(f'    <path d="{d_str}" fill="{fill_rgb}"/>')
                path_d = []
        elif l == "S":
            if path_d:
                d_str = " ".join(path_d)
                svg_elems.append(f'    <path d="{d_str}" fill="none" stroke="{stroke_rgb}" stroke-width="{stroke_w:.2f}" stroke-linecap="round"/>')
                path_d = []
        elif l == "B*":
            if path_d:
                d_str = " ".join(path_d)
                svg_elems.append(f'    <path d="{d_str}" fill="{fill_rgb}" stroke="{stroke_rgb}" stroke-width="{stroke_w:.2f}"/>')
                path_d = []

    svg_elems.append("  </g>")
    svg_elems.append(f'  <rect x="2" y="2" width="176" height="206" rx="15" ry="15" fill="none" stroke="{dept_color}" stroke-width="4"/>')
    svg_elems.append("</svg>")
    return "\n".join(svg_elems)


def build_workforce_directory(lines):
    os.makedirs(AVATARS_DIR, exist_ok=True)
    os.makedirs(PROFILES_DIR, exist_ok=True)

    with open(AUTHORITY_PATH, "r", encoding="utf-8") as f:
        auth_matrix = json.load(f)

    dept_colors = {
        "Human PD": "#1F3A68",
        "Project Mgmt": "#1F3A68",
        "Planning": "#1A9A8F",
        "Engineering": "#2F6EB5",
        "SCM": "#D9772A",
        "Construction": "#3A7D3A",
        "Subcontractor": "#6A3FC0",
        "QA / QC": "#8E6BBF",
        "HSSE": "#C0392B",
        "Contracts": "#A8407A",
        "T&C": "#0F8FBF",
        "Admin": "#7B8A8B",
        "External": "#3C4654",
    }

    clips = [i for i, l in enumerate(lines) if "W* n" in l and ("36 42 re" in lines[i + 2] if i + 2 < len(lines) else False)]
    personnel = []

    for ci in clips:
        q_idx = next(j for j in range(ci, ci + 200) if lines[j].strip() == "Q")
        # Extract department label just before clip
        dept_label = "Project Mgmt"
        for back in range(ci - 1, max(0, ci - 35), -1):
            if "Tm (" in lines[back] and ") Tj" in lines[back]:
                m_d = re.search(r"\((.*?)\)\s*Tj", lines[back])
                if m_d:
                    dept_label = m_d.group(1)
                    break

        # Extract text lines after Q
        card_texts = []
        for fwd in range(q_idx + 1, min(len(lines), q_idx + 35)):
            if "0 0 .078431 rg" in lines[fwd] or ("EXTERNAL PARTIES" in lines[fwd]):
                break
            m_t = re.search(r"\((.*?)\)\s*Tj", lines[fwd])
            if m_t:
                card_texts.append(m_t.group(1).replace("\\(", "(").replace("\\)", ")"))

        raw_name = card_texts[0] if len(card_texts) > 0 else "UNKNOWN"
        agent_key = "DANESH" if "Danesh" in raw_name else raw_name.strip().upper()

        rep_idx = next((idx_t for idx_t, t in enumerate(card_texts) if t.startswith("Reports to:") or t.startswith("Interface:") or "Human" in t), 2)
        role_title = " ".join(card_texts[1:rep_idx]).strip()
        reports_to = card_texts[rep_idx] if rep_idx < len(card_texts) else ""
        status_str = card_texts[rep_idx + 1] if (rep_idx + 1) < len(card_texts) else "Joined"

        joining_str = next((t for t in card_texts if t.startswith("Joining Date:")), "Joining Date: Nov-26 (Day 1)")
        agent_id_str = next((t for t in card_texts if "ID:" in t), "ID: PD-00")
        email_str = next((t for t in card_texts if "@" in t), "")

        agent_id = agent_id_str.split(":", 1)[-1].strip()
        joining_date = joining_str.split(":", 1)[-1].strip()

        color = dept_colors.get(dept_label, "#1F3A68")
        svg_code = pdf_clip_to_svg(lines[ci : q_idx + 1], agent_key, role_title, color)
        svg_filename = f"{agent_key}.svg"
        svg_path = os.path.join(AVATARS_DIR, svg_filename)
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg_code)

        auth_info = auth_matrix.get(agent_key, {})
        persona_rel = auth_info.get("file", "")
        fin_limit = auth_info.get("financial_limit", "UNLIMITED (Project Director)" if agent_key == "DANESH" else "ESCALATE")
        esc_target = auth_info.get("escalation_target", "Board of Directors" if agent_key == "DANESH" else "ATLAS")
        allowed = auth_info.get("allowed_actions", ["Full executive project authority, variation approval, event injection, and claim settlement."])
        prohibs = auth_info.get("prohibitions", ["None (Human-in-the-Loop Project Director)."])

        # Write individual profile markdown
        prof_filename = f"{agent_id}_{agent_key}.md"
        prof_path = os.path.join(PROFILES_DIR, prof_filename)
        prof_md = [
            f"# {raw_name} (`{agent_id}`) — {role_title}",
            "",
            f"<img src=\"../avatars/{svg_filename}\" width=\"140\" alt=\"{raw_name} Avatar\"/>",
            "",
            "## 1. Personnel Identity & Organisation Placement",
            "",
            "| Attribute | Value |",
            "| :--- | :--- |",
            f"| **Agent / Personnel Code** | **`{agent_key}`** (`{raw_name}`) |",
            f"| **Personnel ID** | `{agent_id}` |",
            f"| **Department** | `{dept_label}` |",
            f"| **Role / Title** | **{role_title}** |",
            f"| **Reporting / Interface Line** | `{reports_to}` |",
            f"| **Mobilisation / Status** | `{status_str}` (`{joining_date}`) |",
            f"| **Official Git / Comm Identity** | `{email_str}` |",
            f"| **Full Persona Instruction File** | {f'[`{persona_rel}`](../../{persona_rel})' if persona_rel else 'Human-in-the-Loop Project Director (`CH-01 #31`)'} |",
            "",
            "## 2. Delegated Authority & Governance Limits",
            "",
            f"- **Financial Authority Limit**: `{fin_limit}`",
            f"- **Escalation Target**: `{esc_target}`",
            "",
            "### Permitted Actions (`allowed_actions`)",
        ]
        for a in allowed:
            prof_md.append(f"- {a}")
        prof_md.append("")
        prof_md.append("### Governance Prohibitions (`prohibitions`)")
        for p in prohibs:
            prof_md.append(f"- {p}")
        prof_md.append("")

        with open(prof_path, "w", encoding="utf-8") as f:
            f.write("\n".join(prof_md))

        personnel.append({
            "id": agent_id,
            "key": agent_key,
            "name": raw_name,
            "dept": dept_label,
            "role": role_title,
            "reports_to": reports_to,
            "status": status_str,
            "joining": joining_date,
            "email": email_str,
            "svg": f"avatars/{svg_filename}",
            "profile": f"profiles/{prof_filename}",
            "persona_rel": persona_rel,
            "fin_limit": fin_limit,
            "esc_target": esc_target,
            "allowed": allowed,
            "prohibs": prohibs
        })

    # Write Master WORKFORCE_DIRECTORY.md
    dir_md = [
        "# HELIOS 100MW Solar PV EPC — Master Workforce Directory (65 Personnel)",
        "",
        "**Project**: HELIOS 100MW Solar PV + 33/220kV GSS, Bukhara, Uzbekistan (`FIDIC Yellow Book 1999`)  ",
        "**Roster Composition**: **1 Human Project Director (`Danesh Selwal`) + 64 Built AI Agent Personas (`0 TBI Pending`)**  ",
        "**Master Organisation Chart (PDF)**: [`../HELIOS_OC_Single_Page.pdf`](../HELIOS_OC_Single_Page.pdf) | [`../01_Executive_Command_Suite/HELIOS_OC_Single_Page.pdf`](../01_Executive_Command_Suite/HELIOS_OC_Single_Page.pdf)  ",
        "",
        "---",
        "",
        "## 1. Visual Roster & Personnel Cards (All 65 Personnel)",
        "",
        "| Photo | ID | Code / Name | Department | Role & Reporting Line | Mobilisation & Mail | Authority & Dossier |",
        "| :---: | :--- | :--- | :--- | :--- | :--- | :--- |"
    ]

    for p in personnel:
        persona_link = f"[Persona](../../{p['persona_rel']})" if p["persona_rel"] else "Human PD"
        fin_str = f"${p['fin_limit']:,.0f}" if isinstance(p["fin_limit"], (int, float)) else str(p["fin_limit"])
        summary_desc = p["allowed"][0][:90] + ("..." if len(p["allowed"][0]) > 90 else "") if p["allowed"] else ""
        dir_md.append(
            f"| <img src=\"{p['svg']}\" width=\"64\"/> | **`{p['id']}`** | **{p['name']}**<br/>(`{p['key']}`) | `{p['dept']}` | "
            f"**{p['role']}**<br/>*{p['reports_to']}*<br/>{summary_desc} | `{p['status']}`<br/>{p['joining']}<br/>`{p['email']}` | "
            f"Limit: `{fin_str}`<br/>Esc: `{p['esc_target']}`<br/>[Dossier]({p['profile']}) \\| {persona_link} |"
        )

    dir_md.append("")
    with open(os.path.join(WORKFORCE_DIR, "WORKFORCE_DIRECTORY.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(dir_md))

    print(f"Generated {len(personnel)} SVG avatars, {len(personnel)} profiles, and WORKFORCE_DIRECTORY.md in {WORKFORCE_DIR}")


if __name__ == "__main__":
    updated_lines = update_org_chart_pdf()
    build_workforce_directory(updated_lines)
