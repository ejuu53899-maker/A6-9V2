import os
import logging
import sys
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TradeRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        auth_header = self.headers.get('Authorization', '')

        if not self.validate_auth(auth_header):
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'Unauthorized')
            return

        try:
            data = json.loads(post_data.decode('utf-8'))
            logging.info(f"Received trade data: {data}")
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {"status": "success", "received": data}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Invalid JSON')

    def validate_auth(self, auth_header):
        expected_key = f"Bearer {os.environ.get('JULES_API_KEY_V4', 'JULES_API_KEY_V4_PLACEHOLDER')}"
        return auth_header == expected_key

def validate_api_key(api_key):
    """
    Simulates API key validation for JULES_API_KEY_V4.
    """
    if not api_key:
        logging.error("API Key not found.")
        return False

    if api_key.startswith("JULES_API_KEY_V4_") or api_key == "TEST_KEY":
        logging.info(f"API Key {api_key[:10]}... validated successfully.")
        return True
    else:
        logging.warning(f"Invalid API Key format: {api_key}")
        return False

def start_bridge(api_key, port=8000):
    """
    Starts the bridge and begins listening for data from the MQL5 EA.
    """
    if not validate_api_key(api_key):
        logging.critical("Bridge could not start due to invalid API Key.")
        sys.exit(1)

    server_address = ('', port)
    httpd = HTTPServer(server_address, TradeRequestHandler)
    logging.info(f"GenX Python Bridge V4 starting up on port {port}...")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info("Bridge shutting down.")
        httpd.server_close()

if __name__ == "__main__":
    # Get API key from environment or default for testing
    api_key_v4 = os.environ.get("JULES_API_KEY_V4", "JULES_API_KEY_V4_PLACEHOLDER")

    # Handle command line arguments for override
    if len(sys.argv) > 1:
        api_key_v4 = sys.argv[1]

    start_bridge(api_key_v4)
