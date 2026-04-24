import http.server
import socketserver
import os

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

class EnvReplaceHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            with open('index.html', 'r', encoding='utf-8') as f:
                content = f.read()
            # Replace placeholder
            content = content.replace('$GEMINI_API_KEY', API_KEY)
            self.wfile.write(content.encode('utf-8'))
        else:
            super().do_GET()

with socketserver.TCPServer(("", PORT), EnvReplaceHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
