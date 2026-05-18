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

# Parse Arguments
ENV_FILE=""
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --env) ENV_FILE="$2"; shift ;;
        *) break ;;
    esac
    shift
done

# Load from .env if provided
if [ -f "$ENV_FILE" ]; then
    echo "[INFO] Loading configuration from $ENV_FILE"
    export $(grep -v '^#' "$ENV_FILE" | xargs)
fi

# Load or Request Credentials
JULES_KEY="${1:-$JULES_API_KEY_V4}"
GITHUB_TOKEN="${2:-$GITHUB_TOKEN_PUSH}"
BRIDGE_TYPE="${3:-$BRIDGE_TYPE}"
BRIDGE_TYPE="${BRIDGE_TYPE:-go}"

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

if [ "$BRIDGE_TYPE" == "desktop" ]; then
    echo "Launching All-in-One Desktop Platform..."
    # Check for database in submodule
    if [ ! -f "desktop_mode_repo/genxdb_fx.db" ]; then
        echo "[INFO] Initializing desktop platform database..."
        cd desktop_mode_repo && python3 scripts/setup/setup_database.py && cd ..
    fi
    docker compose up -d desktop-platform
    echo "Desktop platform is running at http://localhost:8080"
    exit 0
fi

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
