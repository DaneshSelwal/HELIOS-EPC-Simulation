#!/usr/bin/env python3
"""
HELIOS EPC Git Pre-Push Hook.
Scans outgoing commits and refuses push if author or committer is "Danesh Selwal"
and the commit touches any path governed by scripts/path_owners.json,
unless the commit message starts with "PD-SETUP:".
"""

import sys
import os
import re
import json
import subprocess

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH_OWNERS_FILE = os.path.join(REPO_ROOT, "scripts", "path_owners.json")

def load_path_rules():
    if not os.path.exists(PATH_OWNERS_FILE):
        return []
    with open(PATH_OWNERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("rules", [])

def path_is_governed(filepath, rules):
    for r in rules:
        pat = r.get("pattern", "")
        if re.search(pat, filepath, re.IGNORECASE):
            return True, r.get("owner"), r.get("description")
    return False, None, None

def check_commit(commit_sha, rules):
    cmd = ["git", "log", "-1", "--format=%an|%ae|%cn|%ce|%s", commit_sha]
    res = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    if res.returncode != 0:
        return True, ""
    
    parts = res.stdout.strip().split("|")
    if len(parts) < 5:
        return True, ""
    an, ae, cn, ce = parts[0], parts[1], parts[2], parts[3]
    msg = parts[4]

    is_danesh = (an == "Danesh Selwal" or cn == "Danesh Selwal" or "selwaldanesh" in ae or "selwaldanesh" in ce)
    if not is_danesh:
        return True, ""
        
    if msg.startswith("PD-SETUP:"):
        return True, ""
        
    diff_cmd = ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", commit_sha]
    diff_res = subprocess.run(diff_cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    touched_files = [line.strip() for line in diff_res.stdout.splitlines() if line.strip()]
    
    for f in touched_files:
        governed, owner, desc = path_is_governed(f, rules)
        if governed:
            err = (
                f"\n[PUSH GUARD REJECTED]\n"
                f"Commit {commit_sha[:7]} by '{an}' touches governed path '{f}' (owned by {owner} - {desc}).\n"
                f"Message: {msg}\n"
                f"Rule: Commits touching simulation project paths must be authored by their owning agent, not 'Danesh Selwal'.\n"
                f"To bypass for deliberate human infrastructure setup, prefix commit message with 'PD-SETUP:'.\n"
            )
            return False, err
            
    return True, ""

def main():
    rules = load_path_rules()
    lines = sys.stdin.read().splitlines()
    for line in lines:
        parts = line.split()
        if len(parts) < 4:
            continue
        local_ref, local_sha, remote_ref, remote_sha = parts[:4]
        
        if local_sha == "0000000000000000000000000000000000000000":
            continue
            
        if remote_sha == "0000000000000000000000000000000000000000":
            cmd = ["git", "rev-list", local_sha, "--not", "--remotes"]
        else:
            cmd = ["git", "rev-list", f"{remote_sha}..{local_sha}"]
            
        res = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
        if res.returncode != 0:
            continue
            
        commit_shas = [c.strip() for c in res.stdout.splitlines() if c.strip()]
        for c in commit_shas:
            ok, err = check_commit(c, rules)
            if not ok:
                print(err, file=sys.stderr)
                sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
