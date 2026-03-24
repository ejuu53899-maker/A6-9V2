import os
import logging
import sys
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global variable to store the validated API key
CONFIGURED_API_KEY = None

class TradeRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        auth_header = self.headers.get('Authorization', '')

        if not self.validate_auth(auth_header):
            logging.warning("Unauthorized access attempt.")
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
        global CONFIGURED_API_KEY
        if not CONFIGURED_API_KEY:
            return False
        expected_key = f"Bearer {CONFIGURED_API_KEY}"
        return auth_header == expected_key

def validate_api_key(api_key):
    """
    Validates the JULES_API_KEY_V4.
    """
    if not api_key or api_key == "YOUR_API_KEY_HERE" or api_key == "JULES_API_KEY_V4_PLACEHOLDER":
        logging.error("Invalid or missing API Key.")
        return False

    # Accept any non-placeholder key
    logging.info(f"API Key starting with {api_key[:5]}... validated successfully.")
    return True

def start_bridge(api_key, port=8000):
    """
    Starts the bridge and begins listening for data from the MQL5 EA.
    """
    global CONFIGURED_API_KEY
    if not validate_api_key(api_key):
        logging.critical("Bridge could not start due to invalid API Key.")
        sys.exit(1)

    CONFIGURED_API_KEY = api_key
    server_address = ('', port)
    httpd = HTTPServer(server_address, TradeRequestHandler)
    logging.info(f"GenX Python Bridge V4 starting up on port {port}...")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info("Bridge shutting down.")
        httpd.server_close()

if __name__ == "__main__":
    # Get API key from environment
    api_key_v4 = os.environ.get("JULES_API_KEY_V4")

    # Handle command line arguments for override
    if len(sys.argv) > 1:
        api_key_v4 = sys.argv[1]

    start_bridge(api_key_v4)
