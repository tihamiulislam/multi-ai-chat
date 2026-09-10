# 🤖 Multi-AI Chat

A multi-agent AI chat application that connects multiple AI models and combines their responses into one final answer.

## 🚀 Overview

Multi-AI Chat sends the user's question to multiple AI agents simultaneously. Their responses are then analyzed and synthesized into a single final answer.

## ✨ Features

- Multi-AI agent architecture
- ChatGPT / OpenAI integration
- Claude / Anthropic integration
- Gemini / Google integration
- Kimi / Moonshot integration
- Parallel AI requests
- AI response synthesis
- Single final answer
- Individual agent responses
- FastAPI backend
- Web-based frontend
- Environment-variable based API keys

## 🛠️ Technologies

- Python
- FastAPI
- Uvicorn
- HTTPX
- HTML
- CSS
- JavaScript
- OpenAI API
- Anthropic API
- Google Gemini API
- Kimi API

## 📁 Project Structure

multi-ai-chat/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

## ⚙️ Installation

### 1. Clone the repository

git clone https://github.com/tihamiulislam/multi-ai-chat.git
cd multi-ai-chat

### 2. Create a virtual environment

Windows:

python -m venv venv

Activate it:

.\venv\Scripts\Activate.ps1

### 3. Install dependencies

pip install -r requirements.txt

### 4. Configure API keys

Create a .env file in the project root:

OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GEMINI_API_KEY=your_gemini_api_key
KIMI_API_KEY=your_kimi_api_key

OPENAI_MODEL=gpt-5
CLAUDE_MODEL=claude-sonnet-4-6
GEMINI_MODEL=gemini-3.7-flash
KIMI_MODEL=kimi-k2.6

Never commit your .env file or API keys to GitHub.

## ▶️ Run the Application

Start the FastAPI server:

python -m uvicorn main:app --reload

Open:

http://127.0.0.1:8000/

API documentation:

http://127.0.0.1:8000/docs

## 🔌 API

### POST /chat

Example request:

{
  "message": "What is artificial intelligence?"
}

The API sends the question to all configured AI agents and returns their individual responses plus one synthesized final answer.

## 📊 Agent Workflow

1. User submits a question.
2. FastAPI receives the request.
3. Four AI agents process the question.
4. Responses are collected.
5. The responses are passed to the synthesis agent.
6. The synthesis agent compares the responses.
7. A single final answer is generated.
8. The frontend displays the final answer.

## 🔐 Security

API keys are stored in environment variables.

The following files should never be committed:

.env
venv/
__pycache__/

Use .env.example as a template.

## 🔮 Future Plans

- Ollama local AI integration
- Run local models without API credits
- Compare mode
- Debate mode
- Multi-agent criticism
- Better response ranking
- Streaming responses
- Conversation history
- User authentication
- Model selection from the UI
- Multiple Ollama agents
- Local/private AI mode
- Cloud deployment

## 🎯 Goal

The goal of this project is to build a personal multi-agent AI system where multiple AI models collaborate to produce a stronger final response than a single model working alone.

## 👨‍💻 Author

Tihami Ul Islam

GitHub:
https://github.com/tihamiulislam

## 📄 License

This project is currently for personal and educational use.
