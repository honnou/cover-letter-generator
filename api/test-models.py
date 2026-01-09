from http.server import BaseHTTPRequestHandler
import json
import os
import anthropic

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            api_key = os.getenv('ANTHROPIC_API_KEY', '')
            
            if not api_key:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'No API key found'}).encode())
                return
            
            # Try to create a client and make a simple request
            client = anthropic.Anthropic(api_key=api_key)
            
            # Try the simplest possible request with different model names
            models_to_try = [
                "claude-sonnet-4.5",
                "claude-4-sonnet",
                "sonnet-4.5",
                "claude-3-sonnet-20240229",
                "claude-3-haiku-20240307"
            ]
            
            results = {}
            for model in models_to_try:
                try:
                    message = client.messages.create(
                        model=model,
                        max_tokens=10,
                        messages=[{"role": "user", "content": "Hi"}]
                    )
                    results[model] = "SUCCESS"
                except Exception as e:
                    results[model] = str(e)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(results, indent=2).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
