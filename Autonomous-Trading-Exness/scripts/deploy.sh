#!/bin/bash
# Deployment helper for GenX FX ZOLO Bridge
# This script handles secret synchronization and pushing to the remote repository

REPO="nuna69v-cell/Autonomous-trading-Exness"

echo "=== GenX FX Deployment Helper ==="

# 1. Sync secrets to GitHub for CI/CD
if [[ -f "./setup-github-secrets.sh" ]]; then
    echo "Syncing repository secrets to $REPO..."
    bash ./setup-github-secrets.sh "$REPO"
else
    echo "Warning: setup-github-secrets.sh not found. Skipping secret sync."
fi

# 2. Check for uncommitted changes
if [[ -n $(git status -s) ]]; then
    echo "Committing recent changes..."
    git add .
    git commit -m "Deployment update: $(date +'%Y-%m-%d %H:%M:%S')"
fi

# 3. Push to main for deployment (triggers Render/Cloud builds)
echo "Pushing changes to remote repository..."
git push origin main

echo "=== Deployment Triggered ==="
echo "Monitor your build at: https://dashboard.render.com/"
