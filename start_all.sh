#!/bin/bash

# Global Startup Orchestration Script for GenX Trading Environment
# Optimized for Mini PC and Cross-Device Execution

echo "=========================================="
echo "   GenX Global System Startup Sequence    "
echo "=========================================="

# Check for resource constraints (common on Mini PCs)
TOTAL_MEM=$(free -m | awk '/^Mem:/{print $2}')
if [ "$TOTAL_MEM" -lt 1000 ]; then
    echo "[WARNING] Low memory detected ($TOTAL_MEM MB). Optimization active."
fi

# Load or Request Credentials
# 1. Check for .env file
if [ -f "GenX_FX_V4/.env" ]; then
    echo "[INFO] Loading credentials from GenX_FX_V4/.env"
    export $(grep -v '^#' GenX_FX_V4/.env | xargs)
fi

JULES_KEY="${1:-$JULES_API_KEY_V4}"
GITHUB_TOKEN="${2:-$GITHUB_TOKEN_PUSH}"
BRIDGE_TYPE="${3:-python}"

if [ -z "$JULES_KEY" ] || [ -z "$GITHUB_TOKEN" ]; then
    echo "[INFO] Tokens not provided. Please enter them below."
    [ -z "$JULES_KEY" ] && read -p "Enter JULES_API_KEY_V4: " JULES_KEY
    [ -z "$GITHUB_TOKEN" ] && read -p "Enter GITHUB_TOKEN_PUSH: " GITHUB_TOKEN
fi

export JULES_API_KEY_V4="$JULES_KEY"
export GITHUB_TOKEN_PUSH="$GITHUB_TOKEN"

# 1. Start Infrastructure (Forgejo/Gitea)
echo "[1/2] Initializing Infrastructure (Docker Compose)..."
if command -v docker-compose &> /dev/null || docker compose version &> /dev/null; then
    docker compose up -d || echo "[ERROR] Failed to start Docker containers. Check Docker status."
else
    echo "[SKIP] Docker Compose not found. Skipping Forgejo startup."
fi

# 2. Start the Selected Bridge
echo "[2/2] Starting Trading Bridge ($BRIDGE_TYPE)..."
if [ "$BRIDGE_TYPE" == "go" ]; then
    echo "Launching High-Performance Go Bridge..."
    if [ -f "./GenX_Go_Bridge/main.go" ]; then
        cd GenX_Go_Bridge && go run main.go
    else
        echo "[ERROR] Go bridge source not found."
        exit 1
    fi
elif [ "$BRIDGE_TYPE" == "python" ]; then
    echo "Launching Flexible Python Bridge..."
    ./GenX_FX_V4/startup.sh "$JULES_KEY" "$GITHUB_TOKEN"
else
    echo "[ERROR] Invalid bridge type. Use 'go' or 'python'."
    exit 1
fi

echo "=========================================="
echo "   Startup Sequence Initiated Successfully "
echo "=========================================="
