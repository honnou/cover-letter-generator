"""
Download cover letter endpoint
"""

from http.server import BaseHTTPRequestHandler
import json
import io
from datetime import datetime
from urllib.parse import urlparse
from _utils import generate_docx, generate_pdf


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Parse request path to get format
            path = urlparse(self.path).path
            format_type = path.split('/')[-1]  # Get last part of path (txt/docx/pdf)

            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))

            text = data.get('text', '')

            if not text:
                self.send_error_response('No text provided', 400)
                return

            # Generate filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

            if format_type == 'txt':
                filename = f'cover_letter_{timestamp}.txt'
                content = text.encode('utf-8')
                mimetype = 'text/plain'

            elif format_type == 'docx':
                filename = f'cover_letter_{timestamp}.docx'
                docx_file = generate_docx(text)
                content = docx_file.read()
                mimetype = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

            elif format_type == 'pdf':
                filename = f'cover_letter_{timestamp}.pdf'
                pdf_file = generate_pdf(text)
                content = pdf_file.read()
                mimetype = 'application/pdf'

            else:
                self.send_error_response('Unsupported format', 400)
                return

            # Send file
            self.send_response(200)
            self.send_header('Content-Type', mimetype)
            self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return

        except Exception as e:
            self.send_error_response(str(e), 500)
            return

    def send_error_response(self, message, code):
        response = {'error': message}
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
