import argparse
import subprocess
import json
import os
import sys

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error running command: {cmd}\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()

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
    
    orig_name = run_cmd("git config user.name || echo 'Danesh Selwal'")
    orig_email = run_cmd("git config user.email || echo 'danesh@example.com'")
    
    try:
        run_cmd(f'git config user.name "{name}"')
        run_cmd(f'git config user.email "{email}"')
        run_cmd(f'git add "{args.file}"')
        run_cmd(f'git commit -m "{args.message}"')
    finally:
        run_cmd(f'git config user.name "{orig_name}"')
        run_cmd(f'git config user.email "{orig_email}"')
        
    print(f"Successfully committed {args.file} as {name}")

if __name__ == "__main__":
    main()
