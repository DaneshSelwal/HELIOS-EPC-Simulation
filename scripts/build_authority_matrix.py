#!/usr/bin/env python3
"""
Extract authority_matrix.json from all 64 persona instruction files across:
  - 00_Project_Overview/ATLAS_ProjectManagement/ (PMO: ATLAS, NEXUS, HERALD)
  - 01_Planning_Controls/ through 10_Subcontractors/
  - 16_External_Parties/ (PATRON, AUDITOR, GRIDMASTER, LUMINOS, INVERSA, POWERTRANS, INSPECTOR, CERTIFIER)
Per agent: role, file, financial_limit, escalation_target, allowed_actions, prohibitions.
Uses 'ESCALATE' where the file gives no financial limit. Does not invent limits.
"""

import glob
import json
import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_ENGINE = os.path.join(REPO_ROOT, "engine", "authority_matrix.json")
OUTPUT_ROOT = os.path.join(REPO_ROOT, "authority_matrix.json")

VALID_ESCALATION_TARGETS = {
    "DANESH", "ATLAS", "NEXUS", "KRONOS", "ARCHON", "CONVOY", "RAMPART",
    "SENTINEL", "AEGIS", "COUNSEL", "IGNITE", "SUMMIT", "BASTION",
    "STRATUM", "CONDUIT", "ARCLINE", "FORTRESS", "SWITCHMAN", "PATRON",
    "FORGE", "PERMIT"
}

def extract_authority_matrix():
    persona_files = sorted(
        glob.glob(os.path.join(REPO_ROOT, "0*", "*_Instructions.md")) +
        glob.glob(os.path.join(REPO_ROOT, "1*", "*_Instructions.md")) +
        glob.glob(os.path.join(REPO_ROOT, "00*", "*", "*_Instructions.md"))
    )

    print(f"Scanning {len(persona_files)} persona files...")

    matrix = {}

    for path in persona_files:
        fname = os.path.basename(path)
        agent = fname.split("_")[0].upper()

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract role from ## ROLE:, # ROLE:, or # AGENT: NAME — ROLE
        role = agent
        role_m = re.search(r"^##?\s*ROLE:\s*([^\n]+)", content, re.MULTILINE)
        if role_m:
            role = role_m.group(1).strip()
        else:
            ag_m = re.search(r"^#\s*AGENT:\s*[A-Za-z0-9_]+\s*[—\-–:]+\s*([^\n]+)", content, re.MULTILINE)
            if ag_m:
                role = ag_m.group(1).strip()

        # Extract Reports To
        rep_m = re.search(r"(?:REPORTS TO(?:\s*\(on site\))?|Reporting to):\s*([^\n]+)", content, re.IGNORECASE)
        reports_to_raw = rep_m.group(1).strip() if rep_m else ""

        # Extract Authority Section
        auth_sec_m = re.search(r"## YOUR AUTHORITY(?: & LIMITS)?(.*?)(?=\n## |\Z)", content, re.DOTALL | re.IGNORECASE)
        auth_text = auth_sec_m.group(1).strip() if auth_sec_m else ""

        # 1. Financial limit extraction
        fin_limit = "ESCALATE"
        fin_matches = re.findall(r'(?:up to|limit of|exceeding|above|threshold of)?\s*(?:USD|\$)\s*([0-9,]+)', auth_text, re.IGNORECASE)
        if fin_matches:
            for fm in fin_matches:
                clean_num = fm.replace(",", "")
                if clean_num.isdigit():
                    num_val = float(clean_num)
                    if 0 < num_val < 5000000.0:
                        fin_limit = num_val
                        break

        # 2. Escalation target extraction
        esc_target = "ATLAS"
        if agent in ["ATLAS", "PATRON", "INSPECTOR", "CERTIFIER", "GRIDMASTER"] or "DANESH" in reports_to_raw.upper():
            esc_target = "DANESH"
        else:
            esc_m = re.search(r'ESCALATE TO\s+([A-Za-z0-9_]+)', auth_text, re.IGNORECASE)
            if esc_m and esc_m.group(1).upper() in VALID_ESCALATION_TARGETS:
                esc_target = esc_m.group(1).upper()
            elif reports_to_raw:
                words = re.findall(r'[A-Za-z0-9_]+', reports_to_raw)
                for w in words:
                    wu = w.upper()
                    if wu in VALID_ESCALATION_TARGETS and wu != agent:
                        esc_target = wu
                        break

        # 3. Allowed action types & Prohibitions extraction
        allowed_actions = []
        prohibitions = []

        # Check inline "(?:- )?You CAN: a; b; c"
        can_inline = re.findall(r'^[-\s*]*?(?:You CAN|Can|Own|Approve|Issue|Lead|Review|Inspect|Track|Maintain|Produce|Compile|Adjudicate|Chair|Order):\s*([^\n]+)', auth_text, re.IGNORECASE | re.MULTILINE)
        for cm in can_inline:
            items = [it.strip() for it in re.split(r'[;]', cm) if it.strip()]
            allowed_actions.extend(items)

        # Check inline "(?:- )?You MUST NOT: a; b; c" or "You CANNOT: a; b; c"
        cant_inline = re.findall(r'^[-\s*]*?(?:You MUST NOT|You CANNOT|You do NOT|You DO NOT|Cannot|Must not|Do not):\s*([^\n]+)', auth_text, re.IGNORECASE | re.MULTILINE)
        for cm in cant_inline:
            items = [it.strip() for it in re.split(r'[;]', cm) if it.strip()]
            prohibitions.extend(items)

        # Also parse multi-line blocks and sentences
        mode = "allowed"
        for line in auth_text.splitlines():
            sline = line.strip()
            if not sline:
                continue
            upper_l = sline.upper()
            if any(h in upper_l for h in ["YOU DO NOT:", "YOU CANNOT", "YOU MUST NOT:", "LIMITS:", "WHAT YOU CANNOT DO", "PROHIBITIONS:"]):
                if ":" in sline and not upper_l.endswith(":"):
                    after = sline.split(":", 1)[1].strip()
                    if after:
                        prohibitions.extend([p.strip() for p in re.split(r'[;]', after) if p.strip()])
                mode = "prohibited"
                continue
            elif any(h in upper_l for h in ["YOU DO:", "YOU CAN:", "AUTHORITY:", "WHAT YOU CAN DO"]):
                if ":" in sline and not upper_l.endswith(":"):
                    after = sline.split(":", 1)[1].strip()
                    if after:
                        allowed_actions.extend([p.strip() for p in re.split(r'[;]', after) if p.strip()])
                mode = "allowed"
                continue
            elif "MUST ESCALATE" in upper_l:
                mode = "escalate"
                continue

            cleaned = sline.lstrip("- *0123456789.).").strip()
            if not cleaned:
                continue

            # Check if line has embedded "You do not ..." or "You cannot ..." sentences
            for sent in re.split(r'(?<=\.)\s+', cleaned):
                sent_s = sent.strip()
                if not sent_s:
                    continue
                if re.match(r'^(?:You\s+)?(?:do\s+not|must\s+not|cannot|never)\b', sent_s, re.IGNORECASE):
                    parts = [p.strip() for p in re.split(r'[;]', sent_s) if p.strip()]
                    prohibitions.extend(parts)
                elif mode == "prohibited":
                    prohibitions.append(sent_s)
                elif mode == "allowed" and not any(k in sent_s.upper() for k in ["YOU CAN:", "YOU MUST ESCALATE", "YOU MUST NOT:", "YOU DO NOT:"]):
                    allowed_actions.append(sent_s)

        # Deduplicate while preserving order
        seen_a = set()
        dedup_allowed = []
        for a in allowed_actions:
            if a not in seen_a and len(a) > 3:
                seen_a.add(a)
                dedup_allowed.append(a)

        seen_p = set()
        dedup_prohib = []
        for p in prohibitions:
            if p not in seen_p and len(p) > 3:
                seen_p.add(p)
                dedup_prohib.append(p)

        matrix[agent] = {
            "agent": agent,
            "role": role,
            "file": os.path.relpath(path, REPO_ROOT),
            "financial_limit": fin_limit,
            "escalation_target": esc_target,
            "allowed_actions": dedup_allowed[:10],
            "prohibitions": dedup_prohib[:8]
        }

    with open(OUTPUT_ENGINE, "w", encoding="utf-8") as f:
        json.dump(matrix, f, indent=2)
    with open(OUTPUT_ROOT, "w", encoding="utf-8") as f:
        json.dump(matrix, f, indent=2)

    print(f"Generated authority_matrix.json with {len(matrix)} agent definitions at:")
    print(f"  - {OUTPUT_ENGINE}")
    print(f"  - {OUTPUT_ROOT}")
    return matrix

if __name__ == "__main__":
    extract_authority_matrix()
