#!/usr/bin/env python3
import argparse
import os
import json
import urllib.request
import urllib.error
import sys

BRIDGE_URL = os.environ.get("GENX_BRIDGE_URL", "http://localhost:8000")
JULES_KEY = os.environ.get("JULES_API_KEY_V4", "JULES_API_KEY_V4_PLACEHOLDER")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN_PUSH", "GITHUB_TOKEN_PUSH_PLACEHOLDER")

def call_bridge(endpoint, method="GET", data=None):
    url = f"{BRIDGE_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {JULES_KEY}",
        "X-GitHub-Token": GITHUB_TOKEN,
        "Content-Type": "application/json"
    }

    req = urllib.request.Request(url, headers=headers, method=method)
    if data:
        req.data = json.dumps(data).encode("utf-8")

    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"Error: {e.code} - {e.read().decode('utf-8')}")
        return None
    except urllib.error.URLError as e:
        print(f"Error connecting to bridge: {e.reason}")
        return None

def status_cmd(args):
    print(f"Checking status at {BRIDGE_URL}/remote/status...")
    result = call_bridge("/remote/status")
    if result:
        print(json.dumps(result, indent=2))
    else:
        print("Failed to retrieve status.")

def signal_check_cmd(args):
    signal_file = "signal_output/genx_signals.json"
    print(f"Checking signals in {signal_file}...")
    if os.path.exists(signal_file):
        try:
            with open(signal_file, "r") as f:
                signals = json.load(f)
                print(json.dumps(signals, indent=2))
        except Exception as e:
            print(f"Error reading signals: {e}")
    else:
        print(f"Signal file {signal_file} not found.")

def control_cmd(args):
    command = args.command.upper()
    print(f"Sending {command} command to bridge...")
    result = call_bridge("/remote/control", method="POST", data={"command": command})
    if result:
        print(f"Successfully sent {command} command.")
        print(json.dumps(result, indent=2))
    else:
        print(f"Failed to send {command} command.")

def main():
    parser = argparse.ArgumentParser(description="Jules CLI for GenX FX V4")
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # Status command
    subparsers.add_parser("status", help="Check bridge status")

    # Signal check command
    subparsers.add_parser("signal-check", help="Check trading signals")

    # Control commands
    subparsers.add_parser("start", help="Start trading")
    subparsers.add_parser("stop", help="Stop trading")
    subparsers.add_parser("pause", help="Pause trading")

    args = parser.parse_args()

    if args.command == "status":
        status_cmd(args)
    elif args.command == "signal-check":
        signal_check_cmd(args)
    elif args.command in ["start", "stop", "pause"]:
        control_cmd(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
