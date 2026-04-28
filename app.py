"""
Gemini Explainer Generator
==========================

A Flask web application for generating AI-powered lesson
introduction texts using Google's Gemini AI. Perfect for
language learning content creators.

Author: CreatorHub Team
Version: 1.0.0
License: MIT

Features:
- AI-powered lesson introduction generation
- Support for 10 languages
- Generates 5 unique options per request
- Simple, natural language output
- One-click copy to clipboard
- Clean, modern UI

Supported Languages:
- French, Spanish, German, Italian, Portuguese
- Japanese, Mandarin Chinese, Korean, Arabic, Russian

Requirements:
- Python 3.8+
- Flask 3.0+
- Google Generative AI SDK
- See requirements.txt for full dependencies

Usage:
    1. Set GEMINI_API_KEY in .env file
    2. Install dependencies: pip install -r requirements.txt
    3. Run: python app.py
    4. Open: http://localhost:5000

API Endpoints:
    POST /api/generate - Generate 5 explainer options
    GET  /api/health   - Health check
    GET  /api/languages - Get supported languages
"""

# =============================================================================
# IMPORTS
# =============================================================================

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
import json
import os
import re

# =============================================================================
# CONFIGURATION
# =============================================================================

# Load environment variables
load_dotenv()

# Application metadata
APP_NAME = "Gemini Explainer Generator"
APP_VERSION = "1.0.0"
APP_AUTHOR = "CreatorHub Team"

# Gemini API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_MODEL = 'gemini-2.0-flash'

# Configure Gemini if API key available
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Supported languages for explainer generation
SUPPORTED_LANGUAGES = [
    {'code': 'fr', 'name': 'French', 'native': 'Francais'},
    {'code': 'es', 'name': 'Spanish', 'native': 'Espanol'},
    {'code': 'de', 'name': 'German', 'native': 'Deutsch'},
    {'code': 'it', 'name': 'Italian', 'native': 'Italiano'},
    {'code': 'pt', 'name': 'Portuguese', 'native': 'Portugues'},
    {'code': 'ja', 'name': 'Japanese', 'native': 'Nihongo'},
    {'code': 'zh', 'name': 'Mandarin Chinese', 'native': 'Zhongwen'},
    {'code': 'ko', 'name': 'Korean', 'native': 'Hangugeo'},
    {'code': 'ar', 'name': 'Arabic', 'native': 'Arabi'},
    {'code': 'ru', 'name': 'Russian', 'native': 'Russkiy'}
]

# Number of explainer options to generate
NUM_OPTIONS = 5

# Word limits for explainers
MIN_WORDS = 15
MAX_WORDS = 25

# =============================================================================
# FLASK APPLICATION SETUP
# =============================================================================

app = Flask(__name__)
CORS(app)

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_language_name(language_input):
    """
    Normalize language input to standard name.
    
    Args:
        language_input (str): Language name or code
        
    Returns:
        str: Normalized language name
    """
    language_lower = language_input.lower().strip()
    
    for lang in SUPPORTED_LANGUAGES:
        if (lang['name'].lower() == language_lower or
            lang['code'].lower() == language_lower or
            lang['native'].lower() == language_lower):
            return lang['name']
    
    return language_input


def validate_language(language):
    """
    Check if language is supported.
    
    Args:
        language (str): Language name
        
    Returns:
        bool: True if supported
    """
    lang_lower = language.lower().strip()
    
    for lang in SUPPORTED_LANGUAGES:
        if (lang['name'].lower() == lang_lower or
            lang['code'].lower() == lang_lower):
            return True
    
    return False


def build_prompt(topic, language):
    """
    Build the AI prompt for generating explainers.
    
    Creates a detailed prompt that instructs the AI to generate
    simple, natural lesson introductions.
    
    Args:
        topic (str): The lesson topic
        language (str): Target language
        
    Returns:
        str: Formatted prompt
    """
    prompt = f"""Generate exactly {NUM_OPTIONS} simple, direct explainer texts for a {language} language learning lesson about "{topic}".

Each explainer should:
- Be very simple and straightforward ({MIN_WORDS}-{MAX_WORDS} words maximum)
- Use plain, natural language like a friendly teacher
- Simply state what students will learn without exaggeration
- Be suitable for language learners of all ages
- Focus on the practical learning outcome

Good examples:
- "Let's learn the names of fruits in French today."
- "Today we'll discover how to talk about colors in Spanish."
- "Learn to identify and name common animals in German."
- "Join us as we explore everyday greetings in Italian."
- "Master the basic numbers from one to ten in Japanese."

Avoid:
- Overly enthusiastic or marketing language
- Complex vocabulary
- Long sentences
- Questions
- Exclamation marks

The explainer text MUST be in English only (not in {language}).

Format your response as a JSON array with exactly {NUM_OPTIONS} strings:
[
  "First explainer text here",
  "Second explainer text here",
  "Third explainer text here",
  "Fourth explainer text here",
  "Fifth explainer text here"
]

Return ONLY the JSON array, no other text, no markdown formatting."""

    return prompt


def parse_json_response(response_text):
    """
    Parse AI response to extract JSON array.
    
    Handles various response formats including:
    - Clean JSON array
    - Markdown code blocks
    - Extra whitespace
    
    Args:
        response_text (str): Raw AI response
        
    Returns:
        list: List of explainer strings
        
    Raises:
        ValueError: If parsing fails
    """
    text = response_text.strip()
    
    # Remove markdown code blocks if present
    if '```json' in text:
        match = re.search(r'```json\s*([\s\S]*?)\s*```', text)
        if match:
            text = match.group(1)
    elif '```' in text:
        match = re.search(r'```\s*([\s\S]*?)\s*```', text)
        if match:
            text = match.group(1)
    
    # Find JSON array boundaries
    start_idx = text.find('[')
    end_idx = text.rfind(']')
    
    if start_idx == -1 or end_idx == -1 or end_idx <= start_idx:
        raise ValueError("No valid JSON array found in response")
    
    json_str = text[start_idx:end_idx + 1]
    
    # Parse JSON
    try:
        result = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {str(e)}")
    
    # Validate result
    if not isinstance(result, list):
        raise ValueError("Response is not a list")
    
    if len(result) != NUM_OPTIONS:
        raise ValueError(f"Expected {NUM_OPTIONS} options, got {len(result)}")
    
    # Validate each item is a string
    for i, item in enumerate(result):
        if not isinstance(item, str):
            raise ValueError(f"Item {i+1} is not a string")
        if len(item.strip()) < 10:
            raise ValueError(f"Item {i+1} is too short")
    
    return result


def call_gemini_api(prompt):
    """
    Call the Gemini API to generate content.
    
    Args:
        prompt (str): The prompt to send
        
    Returns:
        tuple: (success: bool, response_text: str or None, error: str or None)
    """
    if not GEMINI_API_KEY:
        return False, None, "Gemini API key not configured"
    
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        
        if response and response.text:
            return True, response.text, None
        else:
            return False, None, "Empty response from API"
            
    except Exception as e:
        error_msg = str(e)
        
        if "API_KEY" in error_msg.upper():
            return False, None, "Invalid API key"
        elif "QUOTA" in error_msg.upper():
            return False, None, "API quota exceeded"
        elif "RATE" in error_msg.upper():
            return False, None, "Rate limit exceeded. Please wait and try again."
        else:
            return False, None, f"API error: {error_msg}"


def log_generation(topic, language, success, count=0):
    """
    Log a generation operation.
    
    Args:
        topic (str): The topic
        language (str): Target language
        success (bool): Whether generation succeeded
        count (int): Number of options generated
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "SUCCESS" if success else "FAILED"
    topic_preview = topic[:30] + "..." if len(topic) > 30 else topic
    print(f"[{timestamp}] {status}: [{language}] \"{topic_preview}\" -> {count} options")


# =============================================================================
# ROUTE HANDLERS
# =============================================================================

@app.route('/')
def index():
    """
    Render the main application page.
    
    Returns:
        str: Rendered HTML template
    """
    return render_template('index.html')


@app.route('/api/generate', methods=['POST'])
def generate_explainers():
    """
    Generate lesson explainer options using Gemini AI.
    
    Request JSON:
        topic (str): The lesson topic
        language (str): Target language
    
    Returns:
        JSON response with:
        - success (bool)
        - explainers (list): 5 explainer options
        - topic (str): Original topic
        - language (str): Target language
        
    Error Responses:
        400: Missing or invalid input
        500: API or server error
    """
    try:
        # Check API key
        if not GEMINI_API_KEY:
            return jsonify({
                'success': False,
                'error': 'Gemini API key not configured. Please set GEMINI_API_KEY in .env file.'
            }), 500
        
        # Parse request
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        topic = data.get('topic', '').strip()
        language = data.get('language', '').strip()
        
        # Validate inputs
        if not topic:
            return jsonify({
                'success': False,
                'error': 'Topic is required. Please enter a lesson topic.'
            }), 400
        
        if not language:
            return jsonify({
                'success': False,
                'error': 'Language is required. Please select a language.'
            }), 400
        
        # Normalize language name
        language = get_language_name(language)
        
        # Build prompt
        prompt = build_prompt(topic, language)
        
        # Call Gemini API
        success, response_text, error = call_gemini_api(prompt)
        
        if not success:
            log_generation(topic, language, False)
            return jsonify({
                'success': False,
                'error': error
            }), 500
        
        # Parse response
        try:
            explainers = parse_json_response(response_text)
        except ValueError as e:
            log_generation(topic, language, False)
            return jsonify({
                'success': False,
                'error': f'Failed to parse AI response: {str(e)}'
            }), 500
        
        # Log success
        log_generation(topic, language, True, len(explainers))
        
        # Return success response
        return jsonify({
            'success': True,
            'explainers': explainers,
            'topic': topic,
            'language': language
        })
        
    except Exception as e:
        print(f"Error in generate_explainers: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@app.route('/api/languages', methods=['GET'])
def get_languages():
    """
    Get list of supported languages.
    
    Returns:
        JSON response with language information
    """
    return jsonify({
        'languages': SUPPORTED_LANGUAGES,
        'count': len(SUPPORTED_LANGUAGES)
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns:
        JSON response with service status
    """
    return jsonify({
        'status': 'healthy',
        'app_name': APP_NAME,
        'version': APP_VERSION,
        'api_configured': GEMINI_API_KEY is not None,
        'model': GEMINI_MODEL,
        'supported_languages': len(SUPPORTED_LANGUAGES),
        'options_per_request': NUM_OPTIONS
    })


@app.route('/api/info', methods=['GET'])
def get_info():
    """
    Get application information.
    
    Returns:
        JSON response with app metadata
    """
    return jsonify({
        'name': APP_NAME,
        'version': APP_VERSION,
        'author': APP_AUTHOR,
        'model': GEMINI_MODEL,
        'languages': [lang['name'] for lang in SUPPORTED_LANGUAGES],
        'options_per_request': NUM_OPTIONS,
        'word_range': f"{MIN_WORDS}-{MAX_WORDS}"
    })


# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.errorhandler(400)
def bad_request(error):
    """Handle bad request errors."""
    return jsonify({
        'success': False,
        'error': 'Bad request. Please check your input.'
    }), 400


@app.errorhandler(500)
def internal_error(error):
    """Handle internal server errors."""
    return jsonify({
        'success': False,
        'error': 'Internal server error. Please try again.'
    }), 500


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == '__main__':
    # Print startup banner
    print("\n" + "=" * 60)
    print(f"  {APP_NAME}")
    print(f"  Version {APP_VERSION}")
    print("=" * 60)
    print(f"\n  Model: {GEMINI_MODEL}")
    print(f"  Options per request: {NUM_OPTIONS}")
    print(f"\n  Supported Languages ({len(SUPPORTED_LANGUAGES)}):")
    for lang in SUPPORTED_LANGUAGES:
        print(f"    - {lang['name']} ({lang['native']})")
    print(f"\n  API Status:")
    if GEMINI_API_KEY:
        print(f"    Gemini: Configured")
    else:
        print(f"    Gemini: NOT CONFIGURED")
        print(f"    Please set GEMINI_API_KEY in .env file")
    print("\n  Open your browser and go to:")
    print("  http://localhost:5000")
    print("\n  Press Ctrl+C to stop the server")
    print("=" * 60 + "\n")
    
    # Run the Flask development server
    app.run(debug=True, host='0.0.0.0', port=5000)
