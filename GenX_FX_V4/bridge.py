import os
import logging
import sys
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# Configure logging to output structured data
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(threadName)s] - %(message)s',
    stream=sys.stdout
)

class TradeRequestHandler(BaseHTTPRequestHandler):
    def send_json_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                logging.warning("Received request with missing or zero Content-Length.")
                self.send_json_response(400, {"status": "error", "message": "Content-Length required"})
                return

            post_data = self.rfile.read(content_length)

            # Authentication headers
            auth_header = self.headers.get('Authorization', '')
            github_header = self.headers.get('X-GitHub-Token', '')

            if not self.validate_auth(auth_header):
                logging.warning(f"Unauthorized access attempt from {self.client_address[0]}: JULES_API_KEY_V4 mismatch.")
                self.send_json_response(401, {"status": "error", "message": "Invalid JULES_API_KEY_V4"})
                return

            if not self.validate_github_token(github_header):
                logging.warning(f"Unauthorized access attempt from {self.client_address[0]}: GITHUB_TOKEN_PUSH mismatch.")
                self.send_json_response(401, {"status": "error", "message": "Invalid GITHUB_TOKEN_PUSH"})
                return

            try:
                data = json.loads(post_data.decode('utf-8'))
                logging.info(f"Successfully processed trade data from {self.client_address[0]}: {data}")
                self.send_json_response(200, {"status": "success", "received": data})
            except json.JSONDecodeError as e:
                logging.error(f"Failed to decode JSON from {self.client_address[0]}: {e}")
                self.send_json_response(400, {"status": "error", "message": "Invalid JSON format"})
        except Exception as e:
            logging.exception(f"Unexpected error handling POST request from {self.client_address[0]}: {e}")
            self.send_json_response(500, {"status": "error", "message": "Internal server error"})

    def validate_auth(self, auth_header):
        expected_key = f"Bearer {os.environ.get('JULES_API_KEY_V4', 'JULES_API_KEY_V4_PLACEHOLDER')}"
        return auth_header == expected_key

    def validate_github_token(self, github_header):
        expected_github_token = os.environ.get('GITHUB_TOKEN_PUSH', 'GITHUB_TOKEN_PUSH_PLACEHOLDER')
        return github_header == expected_github_token

def validate_tokens(jules_key, github_token):
    if not jules_key:
        logging.error("JULES_API_KEY_V4 not found in environment.")
        return False
    if not github_token:
        logging.error("GITHUB_TOKEN_PUSH not found in environment.")
        return False
    logging.info("Security tokens validated successfully.")
    return True

def start_bridge(port=8000):
    jules_key = os.environ.get("JULES_API_KEY_V4")
    github_token = os.environ.get("GITHUB_TOKEN_PUSH")

    if not validate_tokens(jules_key, github_token):
        logging.critical("Bridge could not start due to missing environment tokens.")
        sys.exit(1)

    server_address = ('', port)
    # Using ThreadingHTTPServer for improved concurrency (Python 3.7+)
    try:
        httpd = ThreadingHTTPServer(server_address, TradeRequestHandler)
    except NameError:
        # Fallback for older Python versions
        from http.server import HTTPServer
        from socketserver import ThreadingMixIn
        class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
            pass
        httpd = ThreadingHTTPServer(server_address, TradeRequestHandler)

    logging.info(f"GenX Python Bridge V4 (Multi-threaded) starting up on port {port}...")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info("Bridge shutting down gracefully.")
        httpd.server_close()

if __name__ == "__main__":
    start_bridge()
