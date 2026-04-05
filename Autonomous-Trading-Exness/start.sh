#!/bin/bash
# Quick Startup Script for GenX FX ZOLO Bridge & Trading System

echo "=== GenX FX Quick Startup ==="

# Check for .env file
if [[ ! -f ".env" ]]; then
    echo "Warning: .env file not found. System may fail to start."
fi

# Export Python Path to include current directory
export PYTHONPATH=$PYTHONPATH:.

# Set default port if not provided
export PORT=${PORT:-8080}

# Define a fallback BRIDGE_API_KEY for testing if not set
if [[ -z "$BRIDGE_API_KEY" && -f .env ]]; then
    # Extract from .env if possible
    ENV_KEY=$(grep BRIDGE_API_KEY .env | cut -d '=' -f2)
    if [[ "$ENV_KEY" != "YOUR_SECURE_BRIDGE_API_KEY" ]]; then
        export BRIDGE_API_KEY=$ENV_KEY
    fi
fi

if [[ -z "$BRIDGE_API_KEY" ]]; then
    echo "Using temporary BRIDGE_API_KEY for startup demo..."
    export BRIDGE_API_KEY="demo_startup_key_$(date +%s)"
fi

# Check for Management Mode argument
if [[ "${1:-}" == "--manage" ]]; then
    echo "Entering GenX FX Management Mode..."
    python3 scripts/management_control.py
    exit 0
fi

echo "Starting GenX FX Autonomous Trading System on port $PORT..."
echo "Bridge Security: ACTIVE"
echo "Tip: Run './start.sh --manage' for control options."

# Start the system
python3 scripts/start_trading.py
