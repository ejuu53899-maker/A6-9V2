import os
import sys

def validate_repo():
    # Files that must exist in the repo
    repo_files = [
        "README.md",
        "requirements.txt",
        "scripts/pr_tool.py",
        "Pr",
        ".github/workflows/ci.yml",
        "config/ea_mapping.json",
        "config/symbols_config.json"
    ]

    # Files that can be local or a template
    optional_or_template_files = [
        (".env", [".env.example", ".env.template"]),
        ("config/vault.json", ["config/vault.json.template"])
    ]

    missing_files = []
    for file in repo_files:
        if not os.path.exists(file):
            missing_files.append(file)

    for file, templates in optional_or_template_files:
        if not os.path.exists(file):
            # Check if at least one template exists
            if not any(os.path.exists(t) for t in templates):
                missing_files.append(f"{file} (or its templates: {', '.join(templates)})")

    if missing_files:
        print("CI Validation FAILED. Missing files:")
        for file in missing_files:
            print(f"  - {file}")
        sys.exit(1)

    print("CI Validation SUCCESS. All required project files or templates present.")
    sys.exit(0)

if __name__ == "__main__":
    validate_repo()
