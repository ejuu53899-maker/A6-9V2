import unittest
import json
import os
import threading
import time
import http.client
from GenX_FX_V4.bridge import TradeRequestHandler, HTTPServer

class TestBridge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set environment variables for testing
        os.environ['JULES_API_KEY_V4'] = 'test_jules_key'
        os.environ['GITHUB_TOKEN_PUSH'] = 'test_github_token'

        cls.port = 8001
        cls.server = HTTPServer(('127.0.0.1', cls.port), TradeRequestHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(1) # Wait for server to start

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()

    def test_get_status(self):
        conn = http.client.HTTPConnection('127.0.0.1', self.port)
        conn.request('GET', '/remote/status')
        response = conn.getresponse()
        data = json.loads(response.read().decode())
        self.assertEqual(response.status, 200)
        self.assertIn('status', data)
        conn.close()

    def test_post_control_unauthorized(self):
        conn = http.client.HTTPConnection('127.0.0.1', self.port)
        conn.request('POST', '/remote/control', body=json.dumps({'command': 'STOP'}))
        response = conn.getresponse()
        self.assertEqual(response.status, 401)
        conn.close()

    def test_post_control_authorized(self):
        headers = {
            'Authorization': 'Bearer test_jules_key',
            'X-GitHub-Token': 'test_github_token',
            'Content-Type': 'application/json'
        }
        conn = http.client.HTTPConnection('127.0.0.1', self.port)
        conn.request('POST', '/remote/control', body=json.dumps({'command': 'STOP'}), headers=headers)
        response = conn.getresponse()
        data = json.loads(response.read().decode())
        self.assertEqual(response.status, 200)
        self.assertEqual(data['operation_status'], 'STOP')
        conn.close()

    def test_post_trade(self):
        headers = {
            'Authorization': 'Bearer test_jules_key',
            'X-GitHub-Token': 'test_github_token',
            'Content-Type': 'application/json'
        }
        payload = {'symbol': 'EURUSD', 'bid': 1.0850}
        conn = http.client.HTTPConnection('127.0.0.1', self.port)
        conn.request('POST', '/trade', body=json.dumps(payload), headers=headers)
        response = conn.getresponse()
        data = json.loads(response.read().decode())
        self.assertEqual(response.status, 200)
        self.assertIn('insights', data)
        conn.close()

    def test_post_performance(self):
        headers = {
            'Authorization': 'Bearer test_jules_key',
            'X-GitHub-Token': 'test_github_token',
            'Content-Type': 'application/json'
        }
        payload = {'account': '12345', 'equity': 10000, 'pnl': 500}
        conn = http.client.HTTPConnection('127.0.0.1', self.port)
        conn.request('POST', '/performance/update', body=json.dumps(payload), headers=headers)
        response = conn.getresponse()
        self.assertEqual(response.status, 200)
        conn.close()

if __name__ == '__main__':
    unittest.main()
