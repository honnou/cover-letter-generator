"""
Generate cover letter endpoint
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import cgi
import io
from ._utils import extract_text_from_file, generate_cover_letter_with_ai


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Parse multipart form data
            content_type = self.headers.get('Content-Type', '')

            if 'multipart/form-data' in content_type:
                # Parse form data
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={
                        'REQUEST_METHOD': 'POST',
                        'CONTENT_TYPE': content_type,
                    }
                )

                # Get text fields
                example_text = form.getvalue('example_text', '')
                job_description_text = form.getvalue('job_description_text', '')

                # Get uploaded files
                if 'example_file' in form:
                    example_file = form['example_file']
                    if example_file.filename:
                        example_text = extract_text_from_file(
                            example_file.file.read(),
                            example_file.filename
                        )

                if 'job_description_file' in form:
                    job_file = form['job_description_file']
                    if job_file.filename:
                        job_description_text = extract_text_from_file(
                            job_file.file.read(),
                            job_file.filename
                        )

                # Validate inputs
                if not example_text or not job_description_text:
                    self.send_error_response(
                        'Both example cover letter and job description are required',
                        400
                    )
                    return

                # Generate new cover letter using AI
                ai_provider = os.getenv('AI_PROVIDER', 'anthropic')
                new_cover_letter = generate_cover_letter_with_ai(
                    example_text,
                    job_description_text,
                    ai_provider
                )

                response = {
                    'success': True,
                    'cover_letter': new_cover_letter
                }

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                return

            else:
                self.send_error_response('Invalid content type', 400)
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
