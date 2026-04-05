#!/bin/bash
# Echo Run / Start Run (F12) Trigger script
# Displays execution status and starts the core trading logic

echo "=== GenX FX Echo Run - Started at $(date) ==="
echo "Python: $(python3 --version)"
echo "Current Branch: $(git rev-parse --abbrev-ref HEAD)"

# Check if startup_config.json exists
if [ ! -f "config/startup_config.json" ]; then
    echo "Warning: config/startup_config.json not found. Initializing migration..."
    python3 scripts/migrate_ea.py
fi

# Run system state extraction to ensure current snapshot
python3 scripts/extract_system_state.py

echo "Starting core trading logic (scripts/start_trading.py)..."
# Start the main trading script in the background with logging
python3 scripts/start_trading.py >> logs/trading_output.log 2>&1 &
TRADING_PID=$!

echo "System started successfully with PID: $TRADING_PID"
echo "Monitor logs at: logs/trading_output.log"
echo "=== Start Run (F12) Triggered ==="
