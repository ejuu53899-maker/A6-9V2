#!/bin/bash

# GenX FX Trading System V4 Startup Script

# Check for arguments or use existing environment variables
JULES_KEY="${1:-$JULES_API_KEY_V4}"
GITHUB_TOKEN="${2:-$GITHUB_TOKEN_PUSH}"
BRIDGE_TYPE="${3:-go}" # Default to Go bridge

# Prompt for tokens if not provided
if [ -z "$JULES_KEY" ]; then
    echo "Enter JULES_API_KEY_V4: "
    read -r JULES_KEY
fi

if [ -z "$GITHUB_TOKEN" ]; then
    echo "Enter GITHUB_TOKEN_PUSH: "
    read -r GITHUB_TOKEN
fi

# Export to environment for the bridge
export JULES_API_KEY_V4="$JULES_KEY"
export GITHUB_TOKEN_PUSH="$GITHUB_TOKEN"

# Log current configuration (masked for security)
echo "------------------------------------------"
echo "GenX FX Bridge V4 Startup Sequence"
echo "------------------------------------------"
echo "JULES_API_KEY_V4:   ${JULES_KEY:0:5}****************"
echo "GITHUB_TOKEN_PUSH:  ${GITHUB_TOKEN:0:5}****************"
echo "Bridge Type:        $BRIDGE_TYPE"
echo "------------------------------------------"

if [ "$BRIDGE_TYPE" == "go" ]; then
    echo "Starting GenX Go Bridge (High Performance)..."
    if [ -f "./GenX_Go_Bridge/genx_bridge" ]; then
        ./GenX_Go_Bridge/genx_bridge
    else
        echo "Go bridge binary not found. Attempting to build..."
        cd GenX_Go_Bridge && go build -o genx_bridge main.go && cd ..
        ./GenX_Go_Bridge/genx_bridge
    fi
elif [ "$BRIDGE_TYPE" == "python" ]; then
    echo "Starting GenX Python Bridge..."
    python3 GenX_FX_V4/bridge.py
else
    echo "Invalid bridge type: $BRIDGE_TYPE. Use 'go' or 'python'."
    exit 1
fi
