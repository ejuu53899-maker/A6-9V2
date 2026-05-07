#!/bin/bash

# GenX FX Trading System V4 Startup Script

# Check for arguments or use existing environment variables
JULES_KEY="${1:-$JULES_API_KEY_V4}"
GITHUB_TOKEN="${2:-$GITHUB_TOKEN_PUSH}"

# Prompt for tokens if not provided
if [ -z "$JULES_KEY" ]; then
    echo "Enter JULES_API_KEY_V4: "
    read -r JULES_KEY
fi

if [ -z "$GITHUB_TOKEN" ]; then
    echo "Enter GITHUB_TOKEN_PUSH: "
    read -r GITHUB_TOKEN
fi

# Load .env if it exists
if [ -f "GenX_FX_V4/.env" ]; then
    export $(grep -v '^#' GenX_FX_V4/.env | xargs)
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
echo "------------------------------------------"

# Ensure dependencies are installed (optional, uncomment if needed)
# pip install -r GenX_FX_V4/requirements.txt

# Start the Python bridge
echo "Starting GenX Python Bridge..."
python3 GenX_FX_V4/bridge.py
