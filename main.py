from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from pathlib import Path
import os
import asyncio
import httpx


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# APP
# ============================================================

app = FastAPI(title="Multi AI Chat")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

INDEX_FILE = FRONTEND_DIR / "index.html"
CSS_FILE = FRONTEND_DIR / "style.css"
JS_FILE = FRONTEND_DIR / "app.js"


# ============================================================
# API KEYS
# ============================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
KIMI_API_KEY = os.getenv("KIMI_API_KEY")


# ============================================================
# MODELS
# ============================================================

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5")

CLAUDE_MODEL = os.getenv(
    "CLAUDE_MODEL",
    "claude-sonnet-4-6"
)

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.7-flash"
)

KIMI_MODEL = os.getenv(
    "KIMI_MODEL",
    "kimi-k2.6"
)


# ============================================================
# REQUEST MODEL
# ============================================================

class ChatRequest(BaseModel):
    message: str


# ============================================================
# OPENAI
# ============================================================

async def ask_openai(message: str):

    if not OPENAI_API_KEY:
        return "OpenAI API key is not configured."

    try:

        async with httpx.AsyncClient(timeout=90) as client:

            response = await client.post(
                "https://api.openai.com/v1/responses",

                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },

                json={
                    "model": OPENAI_MODEL,
                    "input": message
                }
            )

            data = response.json()

            if response.status_code != 200:
                return f"Error: {data}"

            # Responses API output
            for item in data.get("output", []):

                for content in item.get("content", []):

                    if content.get("type") == "output_text":
                        return content.get("text", "")

            return "OpenAI returned no text."

    except Exception as e:

        return f"Error: {str(e)}"


# ============================================================
# CLAUDE
# ============================================================

async def ask_claude(message: str):

    if not ANTHROPIC_API_KEY:
        return "Claude API key is not configured."

    try:

        async with httpx.AsyncClient(timeout=90) as client:

            response = await client.post(
                "https://api.anthropic.com/v1/messages",

                headers={
                    "x-api-key": ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                },

                json={
                    "model": CLAUDE_MODEL,
                    "max_tokens": 2048,
                    "messages": [
                        {
                            "role": "user",
                            "content": message
                        }
                    ]
                }
            )

            data = response.json()

            if response.status_code != 200:
                return f"Error: {data}"

            content = data.get("content", [])

            if content:

                text_parts = []

                for item in content:

                    if item.get("type") == "text":
                        text_parts.append(item.get("text", ""))

                return "\n".join(text_parts)

            return "Claude returned no text."

    except Exception as e:

        return f"Error: {str(e)}"


# ============================================================
# GEMINI
# ============================================================

async def ask_gemini(message: str):

    if not GEMINI_API_KEY:
        return "Gemini API key is not configured."

    try:

        url = (
            f"https://generativelanguage.googleapis.com/"
            f"v1beta/models/{GEMINI_MODEL}:generateContent"
        )

        async with httpx.AsyncClient(timeout=90) as client:

            response = await client.post(

                url,

                headers={
                    "x-goog-api-key": GEMINI_API_KEY,
                    "Content-Type": "application/json"
                },

                json={
                    "contents": [
                        {
                            "parts": [
                                {
                                    "text": message
                                }
                            ]
                        }
                    ]
                }
            )

            data = response.json()

            if response.status_code != 200:
                return f"Error: {data}"

            candidates = data.get("candidates", [])

            if not candidates:
                return "Gemini returned no response."

            parts = candidates[0].get("content", {}).get("parts", [])

            text_parts = []

            for part in parts:

                if "text" in part:
                    text_parts.append(part["text"])

            return "\n".join(text_parts)

    except Exception as e:

        return f"Error: {str(e)}"


# ============================================================
# KIMI
# ============================================================

async def ask_kimi(message: str):

    if not KIMI_API_KEY:
        return "Kimi API key is not configured."

    try:

        async with httpx.AsyncClient(timeout=90) as client:

            response = await client.post(

                "https://api.moonshot.ai/v1/chat/completions",

                headers={
                    "Authorization": f"Bearer {KIMI_API_KEY}",
                    "Content-Type": "application/json"
                },

                json={
                    "model": KIMI_MODEL,

                    "messages": [
                        {
                            "role": "user",
                            "content": message
                        }
                    ]
                }
            )

            data = response.json()

            if response.status_code != 200:
                return f"Error: {data}"

            choices = data.get("choices", [])

            if not choices:
                return "Kimi returned no response."

            return choices[0]["message"]["content"]

    except Exception as e:

        return f"Error: {str(e)}"


# ============================================================
# RUN ALL 4 AGENTS
# ============================================================

async def ask_all_agents(message: str):

    results = await asyncio.gather(

        ask_openai(message),

        ask_claude(message),

        ask_gemini(message),

        ask_kimi(message),

        return_exceptions=True
    )

    return {
        "ChatGPT": (
            str(results[0])
            if not isinstance(results[0], Exception)
            else f"Error: {results[0]}"
        ),

        "Claude": (
            str(results[1])
            if not isinstance(results[1], Exception)
            else f"Error: {results[1]}"
        ),

        "Gemini": (
            str(results[2])
            if not isinstance(results[2], Exception)
            else f"Error: {results[2]}"
        ),

        "Kimi": (
            str(results[3])
            if not isinstance(results[3], Exception)
            else f"Error: {results[3]}"
        )
    }


# ============================================================
# SYNTHESIS
# ============================================================

async def synthesize_with_gemini(
    original_question: str,
    answers: dict
):

    if not GEMINI_API_KEY:
        return "Gemini API key is not configured for synthesis."

    synthesis_prompt = f"""
You are the final synthesis AI in a multi-agent system.

The user asked:

{original_question}


Four AI agents independently answered the question.

========================
CHATGPT
========================

{answers["ChatGPT"]}


========================
CLAUDE
========================

{answers["Claude"]}


========================
GEMINI
========================

{answers["Gemini"]}


========================
KIMI
========================

{answers["Kimi"]}


========================
YOUR TASK
========================

Create ONE final answer for the user.

Rules:

1. Compare all four responses.
2. Identify where they agree.
3. Identify contradictions or questionable claims.
4. Prefer accurate and well-supported information.
5. Do not blindly combine incorrect information.
6. Remove duplicated points.
7. Do not mention the internal multi-agent process unless necessary.
8. Do not say "ChatGPT said", "Claude said", etc.
9. Give the user a clear, useful answer.
10. If the agents disagree, explain the uncertainty briefly.
11. Do not invent information that none of the agents provided.
12. Answer the original question directly.

Return ONLY the final answer.
"""

    try:

        url = (
            f"https://generativelanguage.googleapis.com/"
            f"v1beta/models/{GEMINI_MODEL}:generateContent"
        )

        async with httpx.AsyncClient(timeout=120) as client:

            response = await client.post(

                url,

                headers={
                    "x-goog-api-key": GEMINI_API_KEY,
                    "Content-Type": "application/json"
                },

                json={
                    "contents": [
                        {
                            "parts": [
                                {
                                    "text": synthesis_prompt
                                }
                            ]
                        }
                    ]
                }
            )

            data = response.json()

            if response.status_code != 200:
                return f"Error during synthesis: {data}"

            candidates = data.get("candidates", [])

            if not candidates:
                return "Synthesis AI returned no response."

            parts = candidates[0].get("content", {}).get("parts", [])

            text_parts = []

            for part in parts:

                if "text" in part:
                    text_parts.append(part["text"])

            return "\n".join(text_parts)

    except Exception as e:

        return f"Error during synthesis: {str(e)}"


# ============================================================
# MAIN CHAT ENDPOINT
# ============================================================

@app.post("/chat")
async def chat(request: ChatRequest):

    question = request.message.strip()

    if not question:

        return {
            "error": "Message cannot be empty."
        }


    # STEP 1
    # Ask all 4 agents at the same time

    answers = await ask_all_agents(question)


    # STEP 2
    # Combine the answers into ONE final answer

    final_answer = await synthesize_with_gemini(
        question,
        answers
    )


    # STEP 3
    # Return everything to frontend

    return {

        "question": question,

        "agents": answers,

        "final": final_answer
    }


# ============================================================
# STATUS
# ============================================================

@app.get("/status")
async def status():

    return {

        "application": "Multi AI Chat",

        "agents": {
            "ChatGPT": bool(OPENAI_API_KEY),
            "Claude": bool(ANTHROPIC_API_KEY),
            "Gemini": bool(GEMINI_API_KEY),
            "Kimi": bool(KIMI_API_KEY)
        },

        "models": {
            "ChatGPT": OPENAI_MODEL,
            "Claude": CLAUDE_MODEL,
            "Gemini": GEMINI_MODEL,
            "Kimi": KIMI_MODEL
        }
    }


# ============================================================
# FRONTEND
# ============================================================

@app.get("/")
async def serve_home():

    return FileResponse(INDEX_FILE)


@app.get("/style.css")
async def serve_css():

    return FileResponse(
        CSS_FILE,
        media_type="text/css"
    )


@app.get("/app.js")
async def serve_js():

    return FileResponse(
        JS_FILE,
        media_type="application/javascript"
    )