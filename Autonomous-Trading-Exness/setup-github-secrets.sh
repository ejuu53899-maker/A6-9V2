#!/bin/bash
# Automates setting up GitHub secrets and variables via the gh CLI
# Usage: ./setup-github-secrets.sh <github-repo>
# Example: ./setup-github-secrets.sh nuna69v-cell/ZOLO-A6-9VxNUNA-GenX

if [ -z "$1" ]; then
    echo "Usage: ./setup-github-secrets.sh <github-repo>"
    return 1 2>/dev/null
fi

REPO=$1
echo "Setting up secrets and variables for $REPO..."

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "Error: 'gh' CLI is not installed. Please install it to use this script."
    return 1 2>/dev/null
fi

if [ ! -f .env ]; then
    echo "Error: .env file not found. Please create one from .env.template first."
    return 1 2>/dev/null
fi

echo "Dynamically extracting and syncing secrets from .env..."

# Loop through the .env file, ignoring comments and empty lines
while IFS='=' read -r SECRET VALUE || [ -n "$SECRET" ]; do
    # Trim leading/trailing whitespace
    SECRET=$(echo "$SECRET" | xargs)

    # Remove surrounding quotes from VALUE if present
    VALUE=$(echo "$VALUE" | sed -e 's/^"//' -e 's/"$//' -e "s/^'//" -e "s/'$//")

    # Skip comments and empty lines
    if [[ -z "$SECRET" || "$SECRET" == \#* ]]; then
        continue
    fi

    if [ -n "$VALUE" ]; then
        echo "Setting secret $SECRET..."
        # Use printf to handle special characters in the body
        printf "%s" "$VALUE" | gh secret set "$SECRET" --repo "$REPO"
    else
        echo "Warning: $SECRET is empty in .env. Skipping."
    fi
done < .env

echo "Done."
