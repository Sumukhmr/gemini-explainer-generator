"""
Explainer Generator - AI-Powered Lesson Introductions
======================================================
A Flask web application for generating lesson introduction texts
using Google's Gemini AI.
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Gemini API configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY not set in environment variables!")
else:
    genai.configure(api_key=GEMINI_API_KEY)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/generate', methods=['POST'])
def generate_explainers():
    try:
        if not GEMINI_API_KEY:
            return jsonify({'error': 'Gemini API key not configured'}), 500
        
        data = request.json
        topic = data.get('topic', '')
        language = data.get('language', '')
        
        if not topic or not language:
            return jsonify({'error': 'Topic and language are required'}), 400
        
        # Create the prompt for Gemini
        prompt = f"""Generate exactly 5 simple, direct explainer texts for a {language} language learning lesson about "{topic}".

Each explainer should:
- Be very simple and straightforward (15-25 words maximum)
- Use plain, natural language like a friendly teacher
- Simply state what students will learn without exaggeration
- Examples: "Let's learn fruits in French", "Today we'll learn how to talk about colors in Spanish", "Learn the names of common animals in German"

Keep it simple, clear, and natural. No fancy or over-enthusiastic language, explainer text should be in english strictly.

Format your response as a JSON array with exactly 5 options:
[
  "First explainer text here",
  "Second explainer text here",
  "Third explainer text here",
  "Fourth explainer text here",
  "Fifth explainer text here"
]

Return ONLY the JSON array, no other text."""

        # Generate content using Gemini
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        
        response_text = response.text.strip()
        
        # Extract JSON array from response
        json_match = response_text
        if '```json' in response_text:
            json_match = response_text.split('```json')[1].split('```')[0].strip()
        elif '```' in response_text:
            json_match = response_text.split('```')[1].split('```')[0].strip()
        
        # Find JSON array in the text
        start_idx = json_match.find('[')
        end_idx = json_match.rfind(']') + 1
        
        if start_idx == -1 or end_idx == 0:
            return jsonify({'error': 'Invalid response format from AI'}), 500
            
        json_str = json_match[start_idx:end_idx]
        explainers = json.loads(json_str)
        
        if len(explainers) != 5:
            return jsonify({'error': 'Expected 5 explainers but got a different number'}), 500
        
        return jsonify({
            'success': True,
            'explainers': explainers,
            'topic': topic,
            'language': language
        })
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'api_configured': GEMINI_API_KEY is not None
    })


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("  Explainer Generator - AI-Powered")
    print("=" * 50)
    print("\n  Open your browser and go to:")
    print("  http://localhost:5000")
    print("\n  Press Ctrl+C to stop the server")
    print("=" * 50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
