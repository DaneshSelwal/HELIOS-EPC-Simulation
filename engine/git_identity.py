#!/usr/bin/env python3
"""
HELIOS EPC Single Commit Identity Engine.
Provides commit_as(agent, paths, message) using environment variables:
  GIT_AUTHOR_NAME, GIT_AUTHOR_EMAIL, GIT_COMMITTER_NAME, GIT_COMMITTER_EMAIL
Never modifies local or global git config.
Validates commit identity via git log -1 immediately after committing.
"""

import os
import sys
import json
import subprocess

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDENTITIES_PATH = os.path.join(REPO_ROOT, "scripts", "agent_identities.json")

def load_identities():
    with open(IDENTITIES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_agent_identity(agent_key):
    identities = load_identities()
    norm_key = agent_key.strip().upper()
    if norm_key in identities:
        return identities[norm_key]
    
    # Try normalized replacements
    alt_key = norm_key.replace("_", "-")
    if alt_key in identities:
        return identities[alt_key]
        
    alt_key2 = norm_key.replace("-", "_")
    if alt_key2 in identities:
        return identities[alt_key2]
        
    raise ValueError(f"Agent identity '{agent_key}' not found in {IDENTITIES_PATH}")

def commit_as(agent, paths, message):
    """
    Commits specified paths as the given agent using subprocess environment variables.
    Does NOT modify git config.
    Verifies git log -1 afterwards and raises if identity does not match.
    
    Args:
        agent (str): Agent key (e.g. 'KRONOS', 'SIGMA', 'HELIOS-ENGINE').
        paths (str or list[str]): File path or list of file paths to stage and commit.
        message (str): Commit message.
        
    Returns:
        dict: {'commit_hash': str, 'author': str, 'committer': str, 'message': str}
    """
    identity = get_agent_identity(agent)
    expected_name = identity["name"]
    expected_email = identity["email"]
    
    if isinstance(paths, str):
        paths = [paths]
        
    # Stage specified paths
    for p in paths:
        add_cmd = ["git", "add", "--", p]
        res_add = subprocess.run(add_cmd, cwd=REPO_ROOT, capture_output=True, text=True)
        if res_add.returncode != 0:
            raise RuntimeError(f"git add failed for '{p}': {res_add.stderr}")
            
    # Check if anything is staged
    diff_res = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=REPO_ROOT)
    if diff_res.returncode == 0:
        print(f"Warning: No staged changes for {paths}. Skipping commit.")
        return None

    # Construct clean environment with explicit git author & committer overrides
    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = expected_name
    env["GIT_AUTHOR_EMAIL"] = expected_email
    env["GIT_COMMITTER_NAME"] = expected_name
    env["GIT_COMMITTER_EMAIL"] = expected_email
    
    commit_cmd = ["git", "commit", "-m", message]
    res_commit = subprocess.run(commit_cmd, cwd=REPO_ROOT, env=env, capture_output=True, text=True)
    if res_commit.returncode != 0:
        raise RuntimeError(f"git commit failed for agent '{agent}': {res_commit.stderr}")
        
    # Read back git log -1 verification
    log_cmd = ["git", "log", "-1", "--format=%H|%an|%ae|%cn|%ce|%s"]
    res_log = subprocess.run(log_cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    if res_log.returncode != 0:
        raise RuntimeError(f"Failed to verify commit with git log: {res_log.stderr}")
        
    parts = res_log.stdout.strip().split("|")
    commit_hash, an, ae, cn, ce = parts[0], parts[1], parts[2], parts[3], parts[4]
    subj = parts[5] if len(parts) > 5 else message
    
    if an != expected_name or ae != expected_email or cn != expected_name or ce != expected_email:
        raise RuntimeError(
            f"Commit verification failed for agent '{agent}'!\n"
            f"Expected: {expected_name} <{expected_email}>\n"
            f"Recorded Author: {an} <{ae}>\n"
            f"Recorded Committer: {cn} <{ce}>"
        )
        
    print(f"Successfully committed as {expected_name} <{expected_email}>: {commit_hash[:7]} {subj}")
    return {
        "commit_hash": commit_hash,
        "author": f"{an} <{ae}>",
        "committer": f"{cn} <{ce}>",
        "message": subj
    }

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 engine/git_identity.py <AGENT> <PATH> <MESSAGE>")
        sys.exit(1)
    agent = sys.argv[1]
    path = sys.argv[2]
    msg = sys.argv[3]
    res = commit_as(agent, path, msg)
    print("Result:", res)
