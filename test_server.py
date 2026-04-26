import unittest
import urllib.request
import urllib.error
import threading
import time
import socketserver
import os

# Import the handler and port from our server
from server import ProxyHandler

# Use a different port for testing to avoid conflicts
TEST_PORT = 8002

class TestBallotJourneyServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a dummy .env for testing if it doesn't exist
        if not os.path.exists('.env'):
            with open('.env', 'w') as f:
                f.write('GEMINI_API_KEY=test_key_123\n')
                
        cls.httpd = socketserver.TCPServer(("", TEST_PORT), ProxyHandler)
        cls.server_thread = threading.Thread(target=cls.httpd.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(1) # wait for server to start

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.server_thread.join()

    def test_get_index(self):
        """Test that the server successfully serves index.html"""
        req = urllib.request.Request(f"http://localhost:{TEST_PORT}/")
        try:
            with urllib.request.urlopen(req) as response:
                self.assertEqual(response.status, 200)
                body = response.read().decode('utf-8')
                self.assertIn('<title>The Ballot Journey</title>', body)
        except Exception as e:
            self.fail(f"GET / failed with exception: {e}")

    def test_proxy_rejection_bad_path(self):
        """Test that invalid proxy paths return 404"""
        req = urllib.request.Request(f"http://localhost:{TEST_PORT}/api/invalid/", method='POST')
        try:
            urllib.request.urlopen(req)
            self.fail("Request should have thrown 404 HTTPError")
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 404)

    def test_pwa_files(self):
        """Test that PWA files are accessible"""
        for filename in ['/sw.js', '/manifest.json']:
            req = urllib.request.Request(f"http://localhost:{TEST_PORT}{filename}")
            with urllib.request.urlopen(req) as response:
                self.assertEqual(response.status, 200)
                self.assertGreater(len(response.read()), 0)

    def test_accessibility_elements(self):
        """Test that index.html contains essential accessibility and semantic tags"""
        req = urllib.request.Request(f"http://localhost:{TEST_PORT}/")
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            # Check for semantic main
            self.assertIn('id="main-content"', html)
            # Check for ARIA labels
            self.assertIn('aria-label=', html)
            # Check for skip link
            self.assertIn('class="skip-link"', html)
            # Check for language attribute
            self.assertIn('<html lang="en"', html)

    def test_manifest_validity(self):
        """Test that manifest.json is valid JSON and has required fields"""
        req = urllib.request.Request(f"http://localhost:{TEST_PORT}/manifest.json")
        with urllib.request.urlopen(req) as response:
            manifest = json.loads(response.read().decode('utf-8'))
            self.assertIn('name', manifest)
            self.assertIn('short_name', manifest)
            self.assertIn('display', manifest)


if __name__ == '__main__':
    unittest.main()
