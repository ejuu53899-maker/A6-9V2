#!/usr/bin/env python3
import os
import subprocess
import sys
import re
import argparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ManagementControl")

def run_command(command, capture=True):
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(command, capture_output=capture, text=True, check=True)
        return result.stdout.strip() if capture else ""
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {' '.join(command)}")
        if capture:
            logger.error(f"Error output: {e.stderr}")
        return None
    except FileNotFoundError:
        logger.error(f"Command not found: {command[0]}")
        return None

def get_repo_from_url(url):
    """Robustly extract user/repo from GitHub URLs."""
    if not url:
        return None

    # Matches:
    # https://github.com/user/repo.git
    # https://github.com/user/repo
    # git@github.com:user/repo.git
    # git@github.com:user/repo
    pattern = r"github\.com[:/](.+?)(?:\.git)?$"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def setup_github_secrets(repo=None):
    """Setup GitHub Secrets using the provided GH_TOKEN/GITHUB_PAT."""
    logger.info("Setting up GitHub Secrets...")

    pat = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_PAT")
    if not pat:
        logger.error("No GitHub token found in GH_TOKEN or GITHUB_PAT environment variables.")
        return False

    if not repo:
        # Try to auto-detect repo
        url = run_command(["git", "remote", "get-url", "origin"])
        repo = get_repo_from_url(url)
        if not repo:
            logger.error("Could not auto-detect GitHub repository.")
            return False

    logger.info(f"Using repository: {repo}")

    # Check if gh CLI is installed
    if not run_command(["gh", "--version"]):
        logger.error("gh CLI not found. Please install it first.")
        return False

    # Sync secrets from .env
    if os.path.exists(".env"):
        logger.info("Syncing secrets from .env...")
        # Use the existing script
        result = run_command(["bash", "setup-github-secrets.sh", repo], capture=False)
        if result is not None:
            logger.info("GitHub Secrets setup successfully!")
            return True
    else:
        logger.warning(".env file not found. Skipping secrets sync.")

    return False

def start_system():
    """Launch the trading system."""
    logger.info("Starting GenX FX Trading System...")
    if os.path.exists("start.sh"):
        subprocess.Popen(["bash", "start.sh"])
        logger.info("System launch initiated in the background.")
    else:
        logger.error("start.sh not found.")

def stop_system():
    """Stop the trading system."""
    logger.info("Stopping GenX FX Trading System...")
    # Find PIDs of start_trading.py
    pids = run_command(["pgrep", "-f", "start_trading.py"])
    if pids:
        pid_list = pids.split('\n')
        for pid in pid_list:
            run_command(["kill", pid], capture=False)
        logger.info(f"Terminated PIDs: {', '.join(pid_list)}")
    else:
        logger.info("No active trading process found.")

def automate_pr_merge(message="Automated management update"):
    """Automate the PR/Merge process."""
    logger.info("Starting automated PR and merge...")

    if not os.environ.get("GITHUB_PAT"):
        logger.error("GITHUB_PAT environment variable not set.")
        return False

    if os.path.exists("scripts/pr_tool.py"):
        result = run_command(["python3", "scripts/pr_tool.py", "--message", message], capture=False)
        if result is not None:
            logger.info("PR and Merge completed.")
            return True
    else:
        logger.error("scripts/pr_tool.py not found.")
    return False

def main():
    parser = argparse.ArgumentParser(description="GenX FX Management Control Hub")
    subparsers = parser.add_subparsers(dest="command", help="Management commands")

    # Setup Secrets
    setup_parser = subparsers.add_parser("setup-secrets", help="Setup GitHub Secrets")
    setup_parser.add_argument("--repo", help="Target GitHub repository (user/repo)")

    # Start/Stop
    subparsers.add_parser("start", help="Start the trading system")
    subparsers.add_parser("stop", help="Stop the trading system")

    # PR/Merge
    pr_parser = subparsers.add_parser("pr-merge", help="Automate PR creation and merging")
    pr_parser.add_argument("--message", default="Automated management update", help="Commit message")

    args = parser.parse_args()

    success = False
    if args.command == "setup-secrets":
        success = setup_github_secrets(args.repo)
    elif args.command == "start":
        start_system()
        success = True
    elif args.command == "stop":
        stop_system()
        success = True
    elif args.command == "pr-merge":
        success = automate_pr_merge(args.message)
    else:
        parser.print_help()
        sys.exit(0)

    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
