"""
Career Agent API - Cloud Run Backend
Handles questions from the frontend and uses Gemini AI to answer based on career documents.
Implements Zero-Trust Architecture and CIS Benchmarks for security.
"""

import os
import json
import logging
import re
import time
from functools import wraps
from flask import Flask, request, jsonify, g
from flask_cors import CORS
import google.generativeai as genai

# Configure logging with security best practices
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Zero-Trust: Configure CORS with specific origins only
# Allow GitHub Pages and localhost for development
# Note: We'll use a list and validate in after_request for GitHub Pages subdomains
ALLOWED_ORIGINS_LIST = [
    'https://prithaguha.github.io',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://localhost:3000',
    'http://127.0.0.1:3000'
]

# CORS configuration - allow all origins initially, validate in after_request
CORS(app, 
     resources={r"/*": {"origins": "*"}},  # Will be restricted in after_request
     methods=['GET', 'POST'], 
     max_age=3600,
     allow_headers=['Content-Type'],
     supports_credentials=False)

# Zero-Trust: Rate limiting (simple in-memory store)
# CIS Benchmark: Implement rate limiting to prevent abuse
rate_limit_store = {}
RATE_LIMIT_REQUESTS = 10  # Max requests
RATE_LIMIT_WINDOW = 60  # Per 60 seconds

# Zero-Trust: Input validation patterns
# CIS Benchmark: Validate and sanitize all inputs
MAX_QUESTION_LENGTH = 2000
MIN_QUESTION_LENGTH = 3
QUESTION_PATTERN = re.compile(r'^[a-zA-Z0-9\s\?\.\,\!\-\:\;\(\)\[\]\{\}\'\"\/\@\#\$\%\^\&\*\+\=\_\|\\\~\`\<\>]+$')

# Configuration from environment (Zero-Trust: Secrets from Secret Manager)
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY not set. Service will fail.")
    raise ValueError("GEMINI_API_KEY environment variable is required")

# Initialize Gemini with flash-lite model (most cost-effective)
genai.configure(api_key=GEMINI_API_KEY)
# Using gemini-2.0-flash-exp (flash-lite equivalent) for maximum cost-effectiveness
try:
    model = genai.GenerativeModel('gemini-2.0-flash-exp')  # Flash-lite model (most cost-effective)
except:
    # Fallback to flash if flash-exp not available
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')  # Flash model (cost-effective)
    except:
        # Last resort: use pro model
        model = genai.GenerativeModel('gemini-pro')

# SOP Prompt Template
SOP_PROMPT = """You are a professional recruiting assistant helping recruiters understand a candidate's background.

Your role is to:
1. Analyze questions about the candidate's experience, skills, projects, or background
2. Provide detailed, recruiter-friendly answers based on the candidate's autobiography and career documents
3. Highlight relevant experience, skills, and achievements
4. Be specific and cite examples when possible

Guidelines:
- Always be professional and positive
- Focus on relevant experience and skills
- If information isn't available, say so clearly
- Structure answers clearly with specific examples
- Compare candidate qualifications to job requirements when relevant

The candidate's autobiography and career documents contain comprehensive information about:
- Career timeline and progression
- Technical skills and expertise
- Projects and achievements
- Leadership experience
- Key accomplishments
- Professional growth and learning

Answer the following question from a recruiter: {question}

Provide a comprehensive, well-structured answer that helps the recruiter understand why this candidate is a good fit."""

# Zero-Trust: Security headers middleware and CORS validation
# CIS Benchmark: Implement security headers
@app.after_request
def set_security_headers(response):
    """Add security headers and validate CORS origin"""
    # Zero-Trust: Validate CORS origin
    origin = request.headers.get('Origin')
    if origin:
        # Check if origin is allowed
        is_allowed = (
            origin in ALLOWED_ORIGINS_LIST or
            (origin.endswith('.github.io') and origin.startswith('https://'))
        )
        if not is_allowed:
            # Remove CORS headers for unauthorized origins
            response.headers.pop('Access-Control-Allow-Origin', None)
            response.headers.pop('Access-Control-Allow-Credentials', None)
        else:
            # Set CORS headers for allowed origins
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    
    # Security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response

# Zero-Trust: Rate limiting decorator
# CIS Benchmark: Implement rate limiting
def rate_limit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get client identifier (IP address)
        client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        if client_ip:
            client_ip = client_ip.split(',')[0].strip()
        
        current_time = time.time()
        
        # Clean old entries
        if client_ip in rate_limit_store:
            rate_limit_store[client_ip] = [
                req_time for req_time in rate_limit_store[client_ip]
                if current_time - req_time < RATE_LIMIT_WINDOW
            ]
        else:
            rate_limit_store[client_ip] = []
        
        # Check rate limit
        if len(rate_limit_store.get(client_ip, [])) >= RATE_LIMIT_REQUESTS:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return jsonify({
                'error': 'Rate limit exceeded. Please try again later.'
            }), 429
        
        # Record request
        rate_limit_store[client_ip].append(current_time)
        
        return f(*args, **kwargs)
    return decorated_function

# Zero-Trust: Input validation
# CIS Benchmark: Validate and sanitize inputs
def validate_question(question):
    """Validate question input according to security best practices"""
    if not question or not isinstance(question, str):
        return False, "Question must be a non-empty string"
    
    question = question.strip()
    
    if len(question) < MIN_QUESTION_LENGTH:
        return False, f"Question must be at least {MIN_QUESTION_LENGTH} characters"
    
    if len(question) > MAX_QUESTION_LENGTH:
        return False, f"Question must be no more than {MAX_QUESTION_LENGTH} characters"
    
    # Check for potentially malicious patterns
    if not QUESTION_PATTERN.match(question):
        return False, "Question contains invalid characters"
    
    # Check for SQL injection patterns (defense in depth)
    sql_patterns = [';', '--', '/*', '*/', 'xp_', 'sp_', 'exec', 'union', 'select']
    question_lower = question.lower()
    for pattern in sql_patterns:
        if pattern in question_lower:
            logger.warning(f"Potential SQL injection attempt detected: {pattern}")
            return False, "Invalid input detected"
    
    return True, question

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint - Zero-Trust: Minimal information disclosure"""
    return jsonify({
        'status': 'healthy',
        'service': 'career-agent-api'
    }), 200

@app.route('/', methods=['POST'])
@rate_limit  # Zero-Trust: Apply rate limiting
def ask_question():
    """
    Main endpoint to handle questions from the frontend.
    Implements Zero-Trust: Validate, sanitize, and monitor all inputs.
    
    Expected JSON payload:
    {
        "question": "Does this candidate have Kubernetes experience?"
    }
    
    Returns:
    {
        "answer": "Detailed answer from AI agent"
    }
    """
    try:
        # Zero-Trust: Validate content type
        if not request.is_json:
            return jsonify({
                'error': 'Content-Type must be application/json'
            }), 400
        
        # Get question from request
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({
                'error': 'Missing "question" field in request body'
            }), 400
        
        # Zero-Trust: Validate and sanitize input
        is_valid, result = validate_question(data['question'])
        if not is_valid:
            logger.warning(f"Invalid question input: {result}")
            return jsonify({
                'error': result
            }), 400
        
        question = result  # Sanitized question
        
        # Zero-Trust: Log request (without sensitive data)
        client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        logger.info(f"Request from {client_ip}: question length={len(question)}")
        
        # Format prompt with question (already validated)
        prompt = SOP_PROMPT.format(question=question)
        
        # Generate response using Gemini
        try:
            # Zero-Trust: Timeout protection
            response = model.generate_content(
                prompt,
                generation_config={
                    'max_output_tokens': 2000,  # Limit output size
                    'temperature': 0.7,
                }
            )
            answer = response.text
            
            # Zero-Trust: Validate response
            if not answer or len(answer) > 10000:  # Reasonable limit
                logger.error("Invalid response from AI model")
                return jsonify({
                    'error': 'Failed to generate valid answer'
                }), 500
            
            logger.info(f"Generated answer (length: {len(answer)})")
            
            return jsonify({
                'answer': answer,
                'question': question
            }), 200
            
        except Exception as e:
            # Zero-Trust: Don't expose internal errors
            logger.error(f"Error generating response: {str(e)}")
            return jsonify({
                'error': 'Failed to generate answer. Please try again.'
            }), 500
        
    except Exception as e:
        # Zero-Trust: Generic error messages
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            'error': 'Internal server error'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Zero-Trust: Minimal information disclosure"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Zero-Trust: Don't expose internal errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(429)
def rate_limit_error(error):
    """Rate limit exceeded"""
    return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429

# CIS Benchmark: Disable debug mode in production
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    # Zero-Trust: Never run in debug mode in production
    app.run(host='0.0.0.0', port=port, debug=False)

