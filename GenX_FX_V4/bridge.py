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

        # Authentication headers
        auth_header = self.headers.get('Authorization', '')
        github_header = self.headers.get('X-GitHub-Token', '')

        if self.path == '/ai-trade':
            self.handle_ai_trade(post_data, auth_header)
            return

        if not self.validate_auth(auth_header):
            logging.warning("Unauthorized: JULES_API_KEY_V4 mismatch.")
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'Unauthorized: Invalid JULES_API_KEY_V4')
            return

        if not self.validate_github_token(github_header):
            logging.warning("Unauthorized: GITHUB_TOKEN_PUSH mismatch.")
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'Unauthorized: Invalid GITHUB_TOKEN_PUSH')
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

    def handle_ai_trade(self, post_data, auth_header):
        ai_keys = [
            os.environ.get('AI_API_KEY_1'),
            os.environ.get('AI_API_KEY_2'),
            os.environ.get('AI_API_KEY_3')
        ]

        # Expecting Bearer token for AI agent as well
        provided_key = auth_header.replace('Bearer ', '')

        if provided_key not in ai_keys or not provided_key:
            logging.warning(f"Unauthorized AI Trade attempt with key: {provided_key[:5]}...")
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'Unauthorized AI Agent')
            return

        try:
            data = json.loads(post_data.decode('utf-8'))
            device_id = os.environ.get('DEVICE_ID', 'UNKNOWN')
            logging.info(f"AI Agent Trade Intent received on {device_id}: {data}")

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                "status": "AI_TRADE_RECEIVED",
                "device": device_id,
                "intent": data
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Invalid AI Trade JSON')

    def validate_auth(self, auth_header):
        expected_key = f"Bearer {os.environ.get('JULES_API_KEY_V4', 'JULES_API_KEY_V4_PLACEHOLDER')}"
        return auth_header == expected_key

    def validate_github_token(self, github_header):
        expected_github_token = os.environ.get('GITHUB_TOKEN_PUSH', 'GITHUB_TOKEN_PUSH_PLACEHOLDER')
        return github_header == expected_github_token

def validate_tokens(jules_key, github_token):
    """
    Simulates token validation for startup.
    """
    if not jules_key:
        logging.error("JULES_API_KEY_V4 not found in environment.")
        return False

    if not github_token:
        logging.error("GITHUB_TOKEN_PUSH not found in environment.")
        return False

    logging.info("Startup tokens detected.")
    return True

def start_bridge(port=8000):
    """
    Starts the bridge and begins listening for data from the MQL5 EA.
    """
    jules_key = os.environ.get("JULES_API_KEY_V4")
    github_token = os.environ.get("GITHUB_TOKEN_PUSH")

    if not validate_tokens(jules_key, github_token):
        logging.critical("Bridge could not start due to missing environment tokens.")
        sys.exit(1)

    server_address = ('', port)
    httpd = HTTPServer(server_address, TradeRequestHandler)
    logging.info(f"GenX Python Bridge V4 (Secure) starting up on port {port}...")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info("Bridge shutting down.")
        httpd.server_close()

if __name__ == "__main__":
    start_bridge()
