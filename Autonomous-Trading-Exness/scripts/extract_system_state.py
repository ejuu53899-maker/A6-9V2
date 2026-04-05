import os
import json
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SystemExtractor")

def mask_value(value):
    if not value or len(str(value)) < 4:
        return "[REDACTED]"
    return f"{str(value)[:2]}****{str(value)[-2:]}"

def extract_state():
    load_dotenv()

    snapshot = {
        "system": {
            "os": os.name,
            "cwd": os.getcwd(),
            "python_version": os.sys.version
        },
        "security_profiles": {
            "MT5_ACCOUNT_ID": mask_value(os.getenv("MT5_ACCOUNT_ID")),
            "LOGIN_LIVE_NUMBER": mask_value(os.getenv("LOGIN_LIVE_NUMBER")),
            "TELEGRAM_BOT_TOKEN": mask_value(os.getenv("TELEGRAM_BOT_TOKEN")),
            "BYBIT_API_KEY": mask_value(os.getenv("BYBIT_API_KEY"))
        },
        "infrastructure": {
            "port": os.getenv("PORT", "8080"),
            "bridge_url": f"http://localhost:{os.getenv('PORT', '8080')}"
        },
        "vision_config": {
            "enabled_classes": ["trend", "breakout", "smc"],
            "threshold": 0.75
        }
    }

    with open("SYSTEM_SNAPSHOT.json", "w") as f:
        json.dump(snapshot, f, indent=4)

    logger.info("SYSTEM_SNAPSHOT.json generated successfully.")

if __name__ == "__main__":
    extract_state()
