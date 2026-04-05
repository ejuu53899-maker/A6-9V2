import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("EA-Configurer")

def configure_ea():
    config = {
        "endpoints": {
            "V4": {
                "port": 8000,
                "description": "MetaTrader 5 V4 API Endpoint"
            },
            "Drive": {
                "port": 5500,
                "description": "Google Drive Sync / File Bridge"
            }
        },
        "mappings": [
            {
                "id": "MT5_V4_BRIDGE",
                "internal_port": 8000,
                "container_port": 8000
            },
            {
                "id": "DRIVE_FS_SYNC",
                "internal_port": 5500,
                "container_port": 5500
            }
        ]
    }

    os.makedirs("config", exist_ok=True)
    with open("config/ea_mapping.json", "w") as f:
        json.dump(config, f, indent=4)

    logger.info("config/ea_mapping.json generated successfully.")

if __name__ == "__main__":
    configure_ea()
