import os
import logging
import sys
import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

# Firebase and Google Cloud Storage imports
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import storage

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global State for Analysis and Control
operation_state = {
    "status": "START",
    "last_command_time": datetime.now().isoformat(),
    "command_source": "system"
}
price_history = {} # Key: symbol, Value: list of closing prices

class IndicatorCalculator:
    @staticmethod
    def calculate_sma(prices, period=14):
        if len(prices) < period:
            return None
        return sum(prices[-period:]) / period

    @staticmethod
    def calculate_rsi(prices, period=14):
        if len(prices) < period + 1:
            return None

        gains = []
        losses = []
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))

        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period

        if avg_loss == 0:
            return 100

        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

class TradeRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
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

        auth_header = self.headers.get('Authorization', '')
        github_header = self.headers.get('X-GitHub-Token', '')

        if not self.validate_auth(auth_header):
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'Unauthorized')
            return

        if not self.validate_github_token(github_header):
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'Unauthorized')
            return

        try:
            data = json.loads(post_data.decode('utf-8'))
            insights = {}

            if self.path == '/remote/control':
                self.handle_remote_control(data)
            elif self.path == '/performance/update':
                self.handle_performance_update(data)
            elif self.path == '/trade':
                insights = self.handle_trade_data(data)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                "status": "success",
                "operation_status": operation_state["status"],
                "insights": insights,
                "timestamp": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Invalid JSON')

    def _upload_to_gcs(self, data):
        global gcs_bucket
        if not gcs_bucket:
            return

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            blob_name = f"signals/{data.get('symbol', 'UNKNOWN')}_{timestamp}.json"
            blob = gcs_bucket.blob(blob_name)
            blob.upload_from_string(json.dumps(data), content_type='application/json')
            logging.info(f"✅ Archived to GCS: {blob_name}")
        except Exception as e:
            logging.error(f"Failed to upload to GCS: {e}")

    def handle_trade_data(self, data):
        symbol = data.get('symbol', 'UNKNOWN')
        price = data.get('bid', 0)

        if symbol not in price_history:
            price_history[symbol] = []

        price_history[symbol].append(price)
        if len(price_history[symbol]) > 100:
            price_history[symbol].pop(0)

        sma_14 = IndicatorCalculator.calculate_sma(price_history[symbol], 14)
        rsi_14 = IndicatorCalculator.calculate_rsi(price_history[symbol], 14)

        insights = {
            "symbol": symbol,
            "price": price,
            "sma_14": round(sma_14, 5) if sma_14 else None,
            "rsi_14": round(rsi_14, 2) if rsi_14 else None,
            "signal": "NEUTRAL",
            "timestamp": datetime.now().isoformat()
        }

        if rsi_14:
            if rsi_14 > 70: insights["signal"] = "OVERBOUGHT - Consider SELL"
            elif rsi_14 < 30: insights["signal"] = "OVERSOLD - Consider BUY"

        logging.info(f"📊 Market Insights [{symbol}] - Price: {price}, RSI: {insights['rsi_14']}, Signal: {insights['signal']}")

        # Archive to Cloud Storage
        self._upload_to_gcs(insights)

        return insights

    def handle_performance_update(self, data):
        logging.info(f"📈 Performance - Account: {data.get('account')}, Equity: {data.get('equity')}, PnL: {data.get('pnl')}")

        # Store in Firestore
        global db
        if db:
            try:
                doc_ref = db.collection('performance_v4').document(str(data.get('account', 'unknown')))
                data['last_updated'] = firestore.SERVER_TIMESTAMP
                doc_ref.set(data, merge=True)
                logging.info(f"✅ Performance logged to Firestore for account {data.get('account')}")
            except Exception as e:
                logging.error(f"Failed to log performance to Firestore: {e}")

    def handle_remote_control(self, data):
        global operation_state
        new_status = data.get('command', '').upper()
        if new_status in ["START", "STOP", "PAUSE"]:
            operation_state["status"] = new_status
            operation_state["last_command_time"] = datetime.now().isoformat()
            logging.info(f"🚀 REMOTE CONTROL - New Status: {new_status}")

    def validate_auth(self, auth_header):
        expected_key = f"Bearer {os.environ.get('JULES_API_KEY_V4', 'JULES_API_KEY_V4_PLACEHOLDER')}"
        return auth_header == expected_key

    def validate_github_token(self, github_header):
        expected_github_token = os.environ.get('GITHUB_TOKEN_PUSH', 'GITHUB_TOKEN_PUSH_PLACEHOLDER')
        return github_header == expected_github_token

# Global Cloud Clients
db = None
gcs_bucket = None

def init_cloud_services():
    global db, gcs_bucket

    # Initialize Firebase
    try:
        cred_path = os.environ.get("FIREBASE_SERVICE_ACCOUNT_JSON")
        if cred_path and os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        else:
            # Fallback to default credentials
            firebase_admin.initialize_app()
        db = firestore.client()
        logging.info("Firebase/Firestore initialized.")
    except Exception as e:
        logging.error(f"Failed to initialize Firebase: {e}")

    # Initialize GCS
    try:
        storage_client = storage.Client()
        bucket_name = os.environ.get("GCS_BUCKET_NAME", "genx-trading-signals")
        gcs_bucket = storage_client.bucket(bucket_name)
        logging.info(f"GCS client initialized (Bucket: {bucket_name}).")
    except Exception as e:
        logging.error(f"Failed to initialize GCS: {e}")

def start_bridge(port=8000):
    jules_key = os.environ.get("JULES_API_KEY_V4")
    github_token = os.environ.get("GITHUB_TOKEN_PUSH")

    if not jules_key or not github_token:
        logging.critical("Missing JULES_API_KEY_V4 or GITHUB_TOKEN_PUSH.")
        sys.exit(1)

    init_cloud_services()

    server_address = ('', port)
    httpd = HTTPServer(server_address, TradeRequestHandler)
    logging.info(f"GenX Python Bridge V4 (Secure + Analytics) starting on port {port}...")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info("Bridge shutting down.")
        httpd.server_close()

if __name__ == "__main__":
    start_bridge()
