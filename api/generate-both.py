"""
Generate both cover letter and resume endpoint
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import cgi
import io
import sys

# Add parent directory to path to import _utils
sys.path.insert(0, os.path.dirname(__file__))

from _utils import extract_text_from_file


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
                cover_letter_text = form.getvalue('cover_letter_text', '')
                resume_text = form.getvalue('resume_text', '')
                job_description_text = form.getvalue('job_description_text', '')

                # Get uploaded files
                if 'cover_letter_file' in form:
                    cl_file = form['cover_letter_file']
                    if cl_file.filename:
                        cover_letter_text = extract_text_from_file(
                            cl_file.file.read(),
                            cl_file.filename
                        )

                if 'resume_file' in form:
                    resume_file = form['resume_file']
                    if resume_file.filename:
                        resume_text = extract_text_from_file(
                            resume_file.file.read(),
                            resume_file.filename
                        )

                if 'job_description_file' in form:
                    job_file = form['job_description_file']
                    if job_file.filename:
                        job_description_text = extract_text_from_file(
                            job_file.file.read(),
                            job_file.filename
                        )

                # Validate inputs
                if not cover_letter_text or not resume_text or not job_description_text:
                    self.send_error_response(
                        'Cover letter, resume, and job description are all required',
                        400
                    )
                    return

                # Generate both documents using AI
                ai_provider = os.getenv('AI_PROVIDER', 'anthropic')

                new_cover_letter = self.generate_cover_letter_with_ai(
                    cover_letter_text,
                    job_description_text,
                    ai_provider
                )

                new_resume = self.generate_resume_with_ai(
                    resume_text,
                    job_description_text,
                    ai_provider
                )

                response = {
                    'success': True,
                    'cover_letter': new_cover_letter,
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

    def generate_cover_letter_with_ai(self, example_cover_letter, job_description, ai_provider='anthropic'):
        """Use AI to generate adapted cover letter"""

        # Import AI clients
        import anthropic
        import openai

        ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
        OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

        prompt = f"""You are a professional career advisor. You need to adapt an existing cover letter for a new job opportunity.

EXAMPLE COVER LETTER:
{example_cover_letter}

NEW JOB DESCRIPTION:
{job_description}

Please create a new cover letter for the new job that:
1. Maintains the tone and style of the example cover letter
2. Highlights relevant skills and experiences that match the new job requirements
3. Customizes the content to address the specific role and company
4. Keeps the same general structure and format
5. Is professional, compelling, and tailored to the new position

Please output ONLY the new cover letter text, without any preamble or explanation."""

        try:
            if ai_provider == 'anthropic' and ANTHROPIC_API_KEY:
                anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
                message = anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20241022",
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
                        {"role": "system", "content": "You are a professional career advisor helping to write cover letters."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=2000
                )
                return response.choices[0].message.content

            else:
                # Fallback: Simple template
                return f"""Dear Hiring Manager,

I am writing to express my strong interest in the position described in your job posting. Based on my background and experience, I believe I would be an excellent fit for this role.

The requirements outlined in your job description align well with my skills and career goals.

Thank you for considering my application.

Sincerely,
[Your Name]

---
NOTE: Configure ANTHROPIC_API_KEY or OPENAI_API_KEY for AI-generated content.
"""
        except Exception as e:
            raise Exception(f"Error generating cover letter: {str(e)}")

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
                anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
                message = anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20241022",
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
                # Fallback: Simple template
                return f"""PROFESSIONAL SUMMARY
Experienced professional seeking new opportunities.

RELEVANT EXPERIENCE
{example_resume[:500] if len(example_resume) > 500 else example_resume}

---
NOTE: Configure ANTHROPIC_API_KEY or OPENAI_API_KEY for AI-generated content.
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
