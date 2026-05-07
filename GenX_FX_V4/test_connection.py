import requests
import json
import os
import sys

def test_bridge_connection():
    url = "http://localhost:8000"
    headers = {
        "Authorization": "Bearer test_key",
        "X-GitHub-Token": "test_token",
        "Content-Type": "application/json"
    }
    payload = {
        "symbol": "EURUSDm",
        "bid": 1.0850,
        "ask": 1.0851,
        "lot_size": 0.1,
        "tp": 100.0,
        "sl": 50.0,
        "timestamp": 1715040000
    }

    print(f"Sending test request to {url}...")
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            print("✅ Bridge connection test passed!")
            return True
        else:
            print("❌ Bridge connection test failed.")
            return False
    except Exception as e:
        print(f"❌ Error connecting to bridge: {e}")
        return False

if __name__ == "__main__":
    if not test_bridge_connection():
        sys.exit(1)
