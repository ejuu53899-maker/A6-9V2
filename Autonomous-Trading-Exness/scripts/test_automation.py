import os
import sys

def run_tests():
    print("Running automation tests...")
    # Add basic checks
    checks = [
        ("Checking config directory", os.path.isdir("config")),
        ("Checking scripts directory", os.path.isdir("scripts")),
        ("Checking README.md", os.path.isfile("README.md"))
    ]

    all_passed = True
    for msg, result in checks:
        status = "✓" if result else "✗"
        print(f"{msg}... {status}")
        if not result:
            all_passed = False

    return all_passed

if __name__ == "__main__":
    if not run_tests():
        sys.exit(1)
    sys.exit(0)
