import http.server
import socketserver
import os
import urllib.request
import json

PORT = 8001

# Parse .env
env_vars = {}
try:
    with open('.env', 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split('=', 1)
                if len(parts) == 2:
                    env_vars[parts[0]] = parts[1]
except FileNotFoundError:
    print(".env file not found.")

API_KEY = env_vars.get('GEMINI_API_KEY', '')

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path.startswith('/api/gemini/'):
            # Extract the actual API path
            api_path = self.path.replace('/api/gemini/', '')
            target_url = f"https://generativelanguage.googleapis.com/{api_path}"
            
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else b''
            
            req = urllib.request.Request(target_url, data=post_data, method='POST')
            req.add_header('Content-Type', 'application/json')
            req.add_header('x-goog-api-key', API_KEY)
            req.add_header('x-goog-api-client', 'gemini-javascript')
            
            try:
                with urllib.request.urlopen(req) as response:
                    res_body = response.read()
                    self.send_response(response.status)
                    for header, value in response.headers.items():
                        self.send_header(header, value)
                    self.end_headers()
                    self.wfile.write(res_body)
            except urllib.error.HTTPError as e:
                self.send_response(e.code)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(e.read())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            with open('index.html', 'r', encoding='utf-8') as f:
                content = f.read()
                # Inject environment variables for local testing
                content = content.replace('${GOOGLE_MAPS_API_KEY}', env_vars.get('GOOGLE_MAPS_API_KEY', ''))
                self.wfile.write(content.encode('utf-8'))
        else:
            super().do_GET()

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()
