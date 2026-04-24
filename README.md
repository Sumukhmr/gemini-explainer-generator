# 📝 Explainer Generator

A Flask web application for generating AI-powered lesson introduction texts using Google's Gemini AI. Perfect for language learning content creators.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- **AI-Powered**: Uses Google Gemini AI for intelligent content generation
- **Multiple Languages**: Supports 10 languages including French, Spanish, German, and more
- **5 Options**: Generates 5 unique explainer options to choose from
- **Simple & Natural**: Produces clear, friendly lesson introductions
- **Copy to Clipboard**: Easy one-click copy functionality

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/explainer-generator.git
cd explainer-generator
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```
GEMINI_API_KEY=your_api_key_here
```

### 5. Run the application

```bash
python app.py
```

Open your browser and go to: **http://localhost:5000**

## 📝 Usage

1. **Select Language**: Choose from 10 supported languages
2. **Enter Topic**: Type your lesson topic (e.g., "Fruits", "Colors", "Animals")
3. **Generate**: Click to generate 5 explainer options
4. **Select**: Click on your preferred option
5. **Use**: Copy to clipboard and use in your content

## 🌍 Supported Languages

- 🇫🇷 French
- 🇪🇸 Spanish
- 🇩🇪 German
- 🇮🇹 Italian
- 🇵🇹 Portuguese
- 🇯🇵 Japanese
- 🇨🇳 Mandarin Chinese
- 🇰🇷 Korean
- 🇸🇦 Arabic
- 🇷🇺 Russian

## 🗂️ Project Structure

```
explainer-generator/
├── app.py              # Flask backend
├── templates/
│   └── index.html      # Frontend UI
├── static/             # Static files
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🔑 API Key

Get your Gemini API key from: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

## 💡 Example Output

**Input:**
- Language: French
- Topic: Fruits

**Generated Options:**
1. "Let's learn the names of fruits in French today."
2. "Today we'll discover how to say different fruits in French."
3. "Learn to identify and name common fruits in French."
4. "Join us as we explore fruit vocabulary in French."
5. "Master the French words for your favorite fruits."

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
