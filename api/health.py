"""
Health check endpoint
"""

from http.server import BaseHTTPRequestHandler
import json
import os


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        ai_provider = os.getenv('AI_PROVIDER', 'anthropic')
        anthropic_key = os.getenv('ANTHROPIC_API_KEY', '')
        openai_key = os.getenv('OPENAI_API_KEY', '')

        response = {
            'status': 'healthy',
            'ai_provider': ai_provider,
            'ai_configured': bool(anthropic_key or openai_key)
        }

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
        return
