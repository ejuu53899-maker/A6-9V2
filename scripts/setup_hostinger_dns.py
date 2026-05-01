import os
import sys
import requests
import json

def setup_dns(api_token, domain):
    base_url = "https://api.hostinger.com/api/v1"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    vps_ipv4 = "187.77.140.66"
    vps_ipv6 = "2a02:4780:5e:d1e0::1"

    records = [
        {"type": "A", "name": "@", "content": vps_ipv4, "ttl": 14400},
        {"type": "A", "name": "www", "content": vps_ipv4, "ttl": 14400},
        {"type": "AAAA", "name": "@", "content": vps_ipv6, "ttl": 14400}
    ]

    print(f"Configuring DNS for {domain}...")

    for record in records:
        print(f"Adding/Updating {record['type']} record for {record['name']} -> {record['content']}")
        # In a real scenario, we would first check if the record exists and then PUT or POST
        # For simplicity in this automation, we attempt to update
        endpoint = f"{base_url}/dns/zones/{domain}/records"
        try:
            response = requests.post(endpoint, headers=headers, json=record)
            if response.status_code in [200, 201]:
                print(f"Successfully set {record['type']} record.")
            else:
                print(f"Failed to set {record['type']} record: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error during API request: {e}")

if __name__ == "__main__":
    token = os.environ.get("HOSTINGER_API_TOKEN")
    domain_name = "exness-mt5real24.net"

    if not token:
        print("Error: HOSTINGER_API_TOKEN environment variable is not set.")
        sys.exit(1)

    setup_dns(token, domain_name)
