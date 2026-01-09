"""
Generate resume endpoint
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import cgi
import io
import sys

# Add parent directory to path to import _utils
sys.path.insert(0, os.path.dirname(__file__))

from _utils import extract_text_from_file, generate_cover_letter_with_ai


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
                        'Both example resume and job description are required',
                        400
                    )
                    return

                # Generate new resume using AI
                ai_provider = os.getenv('AI_PROVIDER', 'anthropic')
                new_resume = self.generate_resume_with_ai(
                    example_text,
                    job_description_text,
                    ai_provider
                )

                response = {
                    'success': True,
                    'resume': new_resume
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

    def generate_resume_with_ai(self, example_resume, job_description, ai_provider='anthropic'):
        """Use AI to generate adapted resume"""

        # Import AI clients
        import anthropic
        import openai

        ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
        OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

        prompt = f"""You are a professional career advisor. You need to adapt an existing resume for a new job opportunity.

EXAMPLE RESUME:
{example_resume}

NEW JOB DESCRIPTION:
{job_description}

Please create a new resume for the new job that:
1. Maintains the same professional format and structure
2. Highlights relevant skills and experiences that match the job requirements
3. Reorders or emphasizes experiences that are most relevant to this position
4. Customizes the professional summary or objective to address the specific role
5. Includes relevant keywords from the job description
6. Keeps all information truthful and accurate (no fabrication)

Please output ONLY the new resume text, without any preamble or explanation."""

        try:
            if ai_provider == 'anthropic' and ANTHROPIC_API_KEY:
                client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
                message = client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=2000,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                return message.content[0].text

            elif ai_provider == 'openai' and OPENAI_API_KEY:
                openai.api_key = OPENAI_API_KEY
                response = openai.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a professional career advisor helping to tailor resumes."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=2000
                )
                return response.choices[0].message.content

            else:
                # Fallback: Simple template-based generation (no AI)
                return f"""PROFESSIONAL SUMMARY
{example_resume.split('.')[0] if '.' in example_resume else 'Experienced professional'} seeking new opportunities in the role described.

RELEVANT EXPERIENCE
Based on the job requirements, my background includes relevant experience that aligns with the position.

{example_resume.split('EXPERIENCE')[-1] if 'EXPERIENCE' in example_resume.upper() else example_resume[:500]}

SKILLS
Skills and qualifications matching the job description.

---
NOTE: This is a basic template. Configure ANTHROPIC_API_KEY or OPENAI_API_KEY for AI-generated resumes.
"""
        except Exception as e:
            raise Exception(f"Error generating resume: {str(e)}")

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
