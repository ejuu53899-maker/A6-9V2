#!/usr/bin/env python3
import subprocess
import os
import sys
import json
import urllib.request
import time
import argparse

def run_command(command):
    print(f"Running: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None
    return result.stdout.strip()

def get_repo_name():
    remote_url = run_command(["git", "remote", "get-url", "origin"])
    if not remote_url:
        return None

    # Handle ssh and https URLs
    # e.g., git@github.com:user/repo.git or https://github.com/user/repo.git
    if remote_url.endswith(".git"):
        remote_url = remote_url[:-4]

    parts = remote_url.split("/")
    if len(parts) >= 2:
        return f"{parts[-2].split(':')[-1]}/{parts[-1]}"
    return None

def main():
    parser = argparse.ArgumentParser(description="Automated Push, PR, and Merge tool.")
    parser.add_argument("--repo", help="GitHub repository (user/repo). Auto-detected if not provided.")
    parser.add_argument("--no-merge", action="store_true", help="Do not attempt to merge the PR.")
    parser.add_argument("--wait", type=int, default=5, help="Seconds to wait before merging.")
    parser.add_argument("--message", default="Automated update via Pr tool", help="Commit message.")
    args = parser.parse_args()

    repo = args.repo or get_repo_name()
    if not repo:
        print("Error: Could not detect repository name. Please provide it with --repo.")
        sys.exit(1)

    print(f"Using repository: {repo}")

    token = os.environ.get('GITHUB_PAT') or os.environ.get('GITHUB_TOKEN') or os.environ.get('GIT_PAT')
    if not token:
        print("Error: GITHUB_PAT, GITHUB_TOKEN, or GIT_PAT environment variable not set.")
        sys.exit(1)

    # 1. Get current branch
    branch = run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    if not branch:
        sys.exit(1)

    if branch == "main" or branch == "master":
        print(f"Error: Cannot run Pr tool from {branch} branch directly.")
        sys.exit(1)

    print(f"Current branch: {branch}")

    # 2. Add and commit changes if any
    status = run_command(["git", "status", "--porcelain"])
    if status:
        run_command(["git", "add", "."])
        run_command(["git", "commit", "-m", args.message])
    else:
        print("No changes to commit.")

    # 3. Push to origin
    push_result = run_command(["git", "push", "origin", branch])
    if push_result is None:
        # Try pushing with token in URL if first push failed
        remote_url = f"https://x-access-token:{token}@github.com/{repo}.git"
        run_command(["git", "push", remote_url, branch])

    # 4. Create Pull Request
    print("Creating Pull Request...")
    pr_url = f"https://api.github.com/repos/{repo}/pulls"
    pr_data = {
        "title": args.message,
        "head": branch,
        "base": "main",
        "body": "Automated Pull Request created by Jules."
    }

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }

    req = urllib.request.Request(pr_url, data=json.dumps(pr_data).encode(), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as f:
            res = json.loads(f.read().decode())
            pr_number = res['number']
            print(f"Pull Request created: {res['html_url']} (Number: {pr_number})")
    except Exception as e:
        # Check if PR already exists
        if hasattr(e, 'read'):
            error_msg = e.read().decode()
            if "A pull request already exists" in error_msg:
                print("Pull request already exists. Fetching existing PR...")
                # Search for existing PR
                search_url = f"https://api.github.com/repos/{repo}/pulls?head={repo.split('/')[0]}:{branch}"
                search_req = urllib.request.Request(search_url, headers=headers)
                with urllib.request.urlopen(search_req) as search_f:
                    search_res = json.loads(search_f.read().decode())
                    if search_res:
                        pr_number = search_res[0]['number']
                        print(f"Found existing PR #{pr_number}: {search_res[0]['html_url']}")
                    else:
                        print("Failed to find existing PR.")
                        sys.exit(1)
            else:
                print(f"Failed to create PR: {e} - {error_msg}")
                sys.exit(1)
        else:
            print(f"Failed to create PR: {e}")
            sys.exit(1)

    if args.no_merge:
        print("Merge skipped as requested.")
        return

    # 5. Merge Pull Request
    print(f"Merging Pull Request #{pr_number}...")
    merge_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/merge"
    merge_data = {
        "commit_title": f"Automated merge of {branch}",
        "merge_method": "squash"
    }

    # Wait as requested
    if args.wait > 0:
        print(f"Waiting {args.wait} seconds for CI/checks...")
        time.sleep(args.wait)

    req = urllib.request.Request(merge_url, data=json.dumps(merge_data).encode(), headers=headers, method="PUT")
    try:
        with urllib.request.urlopen(req) as f:
            res = json.loads(f.read().decode())
            if res.get('merged'):
                print("Pull Request merged successfully!")
            else:
                print(f"Merge failed: {res.get('message')}")
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode()
        print(f"Failed to merge PR: {e.code} - {error_msg}")
        if e.code == 405:
            print("Hint: PR might not be mergeable yet (CI failing or still in progress).")
        sys.exit(1)
    except Exception as e:
        print(f"Failed to merge PR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
