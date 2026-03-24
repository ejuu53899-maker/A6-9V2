import os
import logging
import sys
import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global Operation State for Remote Control
operation_state = {
    "status": "START",  # Possible: START, STOP, PAUSE
    "last_command_time": datetime.now().isoformat(),
    "command_source": "system"
}

class TradeRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Handle remote status checks (e.g., from EA)
        if self.path == '/remote/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(operation_state).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Authentication headers
        auth_header = self.headers.get('Authorization', '')
        github_header = self.headers.get('X-GitHub-Token', '')

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

            # Route requests
            if self.path == '/remote/control':
                self.handle_remote_control(data)
            elif self.path == '/performance/update':
                self.handle_performance_update(data)
            else:
                self.handle_trade_data(data)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {"status": "success", "operation_status": operation_state["status"], "timestamp": datetime.now().isoformat()}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Invalid JSON')

    def handle_trade_data(self, data):
        logging.info(f"Received trade data: {data}")

    def handle_performance_update(self, data):
        logging.info(f"📈 Performance Update - Account: {data.get('account')}, Balance: {data.get('balance')}, Equity: {data.get('equity')}, PnL: {data.get('pnl')}")

    def handle_remote_control(self, data):
        global operation_state
        new_status = data.get('command', '').upper()
        if new_status in ["START", "STOP", "PAUSE"]:
            operation_state["status"] = new_status
            operation_state["last_command_time"] = datetime.now().isoformat()
            operation_state["command_source"] = data.get('source', 'remote_control')
            logging.info(f"🚀 REMOTE CONTROL - New Status: {new_status} (Source: {operation_state['command_source']})")
        else:
            logging.warning(f"Invalid Remote Control command: {new_status}")

    def validate_auth(self, auth_header):
        expected_key = f"Bearer {os.environ.get('JULES_API_KEY_V4', 'JULES_API_KEY_V4_PLACEHOLDER')}"
        return auth_header == expected_key

    def validate_github_token(self, github_header):
        expected_github_token = os.environ.get('GITHUB_TOKEN_PUSH', 'GITHUB_TOKEN_PUSH_PLACEHOLDER')
        return github_header == expected_github_token

def start_bridge(port=8000):
    jules_key = os.environ.get("JULES_API_KEY_V4")
    github_token = os.environ.get("GITHUB_TOKEN_PUSH")

    if not jules_key or not github_token:
        logging.critical("Missing JULES_API_KEY_V4 or GITHUB_TOKEN_PUSH.")
        sys.exit(1)

    server_address = ('', port)
    httpd = HTTPServer(server_address, TradeRequestHandler)
    logging.info(f"GenX Python Bridge V4 (Secure + Performance + Remote Control) starting on port {port}...")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info("Bridge shutting down.")
        httpd.server_close()

if __name__ == "__main__":
    start_bridge()
