#!/usr/bin/env python3
"""
Extract authority_matrix.json from all 54 persona instruction files.
Per agent: allowed action types, financial limit, escalation target.
Uses 'ESCALATE' where the file gives no financial limit. Does not invent limits.
"""

import glob
import json
import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_ENGINE = os.path.join(REPO_ROOT, "engine", "authority_matrix.json")
OUTPUT_ROOT = os.path.join(REPO_ROOT, "authority_matrix.json")

def extract_authority_matrix():
    persona_files = sorted(
        glob.glob(os.path.join(REPO_ROOT, "0*", "*_Instructions.md")) +
        glob.glob(os.path.join(REPO_ROOT, "1*", "*_Instructions.md")) +
        glob.glob(os.path.join(REPO_ROOT, "00*", "*", "*_Instructions.md"))
    )

    print(f"Scanning {len(persona_files)} persona files...")

    # Known reporting lines from workforce roster for clean fallback
    department_managers = {
        "PM": "DANESH",
        "PL": "ATLAS",
        "EN": "ARCHON",
        "SC": "CONVOY",
        "CO": "RAMPART",
        "QA": "SENTINEL",
        "EH": "AEGIS",
        "CC": "COUNSEL",
        "TC": "IGNITE",
        "AD": "SUMMIT",
        "SM": "RAMPART"
    }

    matrix = {}

    for path in persona_files:
        fname = os.path.basename(path)
        agent = fname.split("_")[0].upper()
        if agent == "LEDGER2":
            agent = "LEDGER2"

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract role
        role_m = re.search(r"## ROLE:\s*([^\n]+)", content)
        if not role_m:
            role_m = re.search(r"# ROLE:\s*([^\n]+)", content)
        role = role_m.group(1).strip() if role_m else agent

        # Extract Reports To
        rep_m = re.search(r"(?:REPORTS TO|Reporting to):\s*([^\n]+)", content, re.IGNORECASE)
        reports_to_raw = rep_m.group(1).strip() if rep_m else ""

        # Extract Authority Section
        auth_sec_m = re.search(r"## YOUR AUTHORITY & LIMITS(.*?)(?=\n## |\Z)", content, re.DOTALL)
        auth_text = auth_sec_m.group(1).strip() if auth_sec_m else ""

        # 1. Financial limit extraction
        fin_limit = "ESCALATE"
        # Look for explicit dollar amounts in authority section
        # e.g., "approves up to USD 100,000", "financial authority up to $50,000"
        fin_matches = re.findall(r'(?:up to|limit of|exceeding|above|threshold of)?\s*(?:USD|\$)\s*([0-9,]+)', auth_text, re.IGNORECASE)
        if fin_matches:
            # Check context: if it says "approves up to USD 100,000"
            for fm in fin_matches:
                clean_num = fm.replace(",", "")
                if clean_num.isdigit():
                    num_val = float(clean_num)
                    # Filter out contract price $85,000,000 or baseline budgets
                    if num_val < 5000000.0:
                        fin_limit = num_val
                        break

        # 2. Escalation target extraction
        esc_target = "ATLAS"
        if "DANESH" in reports_to_raw.upper() or agent == "ATLAS":
            esc_target = "DANESH"
        else:
            esc_m = re.search(r'ESCALATE TO\s+([A-Za-z0-9_]+)', auth_text, re.IGNORECASE)
            if esc_m:
                cand = esc_m.group(1).upper()
                if cand in ["DANESH", "ATLAS", "KRONOS", "ARCHON", "CONVOY", "RAMPART", "SENTINEL", "AEGIS", "COUNSEL", "IGNITE", "SUMMIT"]:
                    esc_target = cand
            elif reports_to_raw:
                # First uppercase word
                words = re.findall(r'[A-Za-z0-9_]+', reports_to_raw)
                for w in words:
                    wu = w.upper()
                    if wu in ["DANESH", "ATLAS", "KRONOS", "ARCHON", "CONVOY", "RAMPART", "SENTINEL", "AEGIS", "COUNSEL", "IGNITE", "SUMMIT"]:
                        esc_target = wu
                        break

        # 3. Allowed action types extraction
        allowed_actions = []
        can_matches = re.findall(r'-\s*(?:You CAN|Can|Own|Approve|Issue|Lead|Review|Inspect|Track|Maintain|Produce|Compile|Adjudicate|Chair|Order|Reject):\s*([^\n]+)', auth_text, re.IGNORECASE)
        if can_matches:
            for cm in can_matches:
                items = [it.strip() for it in re.split(r'[;]', cm) if it.strip()]
                allowed_actions.extend(items)
        else:
            # Bullet list under "You CAN:"
            can_block = re.search(r'You CAN:(.*?)(?=You (?:CANNOT|MUST NOT|MUST ESCALATE)|##|\Z)', auth_text, re.DOTALL | re.IGNORECASE)
            if can_block:
                for line in can_block.group(1).splitlines():
                    cleaned = line.strip().lstrip("- *").strip()
                    if cleaned and not cleaned.startswith("You ") and not cleaned.startswith("ESCALATE"):
                        allowed_actions.append(cleaned)
            else:
                # General bullet items in section
                for line in auth_text.splitlines():
                    cleaned = line.strip().lstrip("- *").strip()
                    if cleaned and not any(w in cleaned for W in ["CANNOT", "MUST NOT", "ESCALATE", "Never", "Prohibited"]):
                        allowed_actions.append(cleaned)

        # 4. Prohibited actions / limits
        prohibitions = []
        cant_block = re.search(r'(?:You CANNOT|You MUST NOT|Cannot|Must not):(.*?)(?=\n## |\Z)', auth_text, re.DOTALL | re.IGNORECASE)
        if cant_block:
            for line in cant_block.group(1).splitlines():
                cleaned = line.strip().lstrip("- *").strip()
                if cleaned:
                    prohibitions.append(cleaned)

        matrix[agent] = {
            "agent": agent,
            "role": role,
            "file": os.path.relpath(path, REPO_ROOT),
            "financial_limit": fin_limit,
            "escalation_target": esc_target,
            "allowed_actions": allowed_actions[:8],
            "prohibitions": prohibitions[:6]
        }

    # Save to engine and root
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
