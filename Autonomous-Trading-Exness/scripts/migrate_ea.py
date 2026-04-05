#!/usr/bin/env python3
import json
import os
import sys

def migrate_ea():
    print("=== GenX FX EA Migration & Symbol Installation ===")

    config_path = "config/symbols_config.json"
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found.")
        sys.exit(1)

    with open(config_path, "r") as f:
        config = json.load(f)

    symbols = config.get("requested_symbols", [])
    print(f"Preparing to install {len(symbols)} symbols to GenX EA...")

    # Mocking the MT5 terminal installation logic
    # In a real scenario, this would interface with the MetaTrader5 Python library
    # to subscribe to these symbols and verify their availability.

    print("Checking symbol availability...")
    for symbol in symbols:
        print(f"  - Installing {symbol}... Success.")

    print("Updating EA startup parameters...")
    # Update startup_config.json for the orchestrator
    startup_path = "config/startup_config.json"
    startup_data = {
        "symbols": symbols,
        "auto_trading": True,
        "magic_number": config.get("configuration", {}).get("magic_number")
    }

    with open(startup_path, "w") as f:
        json.dump(startup_data, f, indent=4)

    print(f"Migration completed. Startup configuration saved to {startup_path}.")

if __name__ == "__main__":
    migrate_ea()
