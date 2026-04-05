#!/bin/bash
# GenX FX Primary 'Quick Start' Entry Point
# Automates venv creation, dependencies, and system execution

VENV_DIR="venv"

# 1. Virtual Environment Setup
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
fi

# 2. Activate Venv and Install Dependencies
source $VENV_DIR/bin/activate
echo "Installing/Updating dependencies..."
pip install -r requirements.txt

# 3. Environment Check
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    echo "Copying .env.example to .env..."
    cp .env.example .env
fi

# 4. System Execution
export PYTHONPATH=$PYTHONPATH:.
echo "Launching GenX FX Autonomous Trading System..."
python3 scripts/start_trading.py
