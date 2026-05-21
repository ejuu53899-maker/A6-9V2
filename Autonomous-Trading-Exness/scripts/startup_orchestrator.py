import os
import subprocess
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def start_system():
    logging.info("Starting GenX FX Trading Orchestrator...")

    # Check for core dependencies
    if os.path.exists("scripts/start_trading.py"):
        logging.info("Starting market monitoring...")
        subprocess.Popen(["python3", "scripts/start_trading.py"])
    else:
        logging.error("Missing scripts/start_trading.py")

    logging.info("System kickstarted successfully.")

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        logging.info("Shutting down orchestrator...")

if __name__ == "__main__":
    start_system()
