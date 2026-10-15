#!/usr/bin/env python3
"""
Thin wrapper around engine.git_identity.commit_as.
"""

import argparse
import json
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

from engine.git_identity import commit_as

def main():
    parser = argparse.ArgumentParser(description="Commit file as a specific agent.")
    parser.add_argument("--agent", required=True, help="Agent name")
    parser.add_argument("--message", required=True, help="Commit message")
    parser.add_argument("--file", required=True, help="File to commit")
    args = parser.parse_args()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "agent_identities.json"), "r") as f:
        identities = json.load(f)

    if args.agent not in identities:
        print(f"Error: Identity for {args.agent} not found.")
        sys.exit(1)

    identity = identities[args.agent]
    name = identity["name"]
    email = identity["email"]

    commit_as(agent=args.agent, paths=args.file, message=args.message)

if __name__ == "__main__":
    main()
