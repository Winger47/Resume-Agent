# Resume Analyser

A FastAPI application for analysing resumes against job descriptions using an AI-powered chat interface.

## Features

- Upload a PDF resume with drag & drop
- Paste a job description to set context
- Start an AI chat session powered by Groq LLM
- Ask anything — skills match, gaps, tailoring tips, interview prep
- Session management via Redis (no login required)
- Clean, minimal chat UI served directly by the API

## How it works

1. User uploads a PDF resume and pastes a job description on the upload screen
2. `POST /chat/start` parses the PDF, stores resume + JD in Redis, returns a `session_id`
3. The chat screen opens — user asks questions in natural language
4. `POST /chat/message` sends each message to the Groq LLM with the resume/JD context
5. AI responses stream back as chat bubbles

## Project structure

```
resume-analyser/
├── app/
│   ├── main.py           # FastAPI app, endpoint definitions
│   ├── chat_agent.py     # LLM chat logic (Groq)
│   ├── session_manager.py# Redis session store (resume + JD)
│   ├── agent.py          # Agentic analysis runner
│   ├── extractor.py      # Skill extraction from text
│   ├── matcher.py        # Resume-to-JD skill matching
│   └── ai_agent.py       # Suggestion generation
├── index.html            # Chat UI (single-file, no frameworks)
├── .env                  # API keys (not committed)
├── requirements.txt      # Python dependencies
└── .venv/                # Virtual environment (not committed)
```

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Serves the chat UI (`index.html`) |
| `POST` | `/chat/start` | Upload PDF + JD, returns `session_id` |
| `POST` | `/chat/message` | Send a message, returns AI response |
| `POST` | `/analyse/` | Legacy: skill match score + suggestions |
| `POST` | `/analyse_text/` | Legacy: agentic text analysis |
| `GET` | `/health` | Health check |

### POST /chat/start

**Form data:** `file` (PDF), `jd_text` (string)  
**Returns:** `{ "session_id": "uuid-string" }`

### POST /chat/message

**Form data:** `session_id` (string), `message` (string)  
**Returns:** `{ "response": "LLM response text" }`

## Setup

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your API keys:
   ```
   GROQ_API_KEY=your_groq_api_key
   ```

4. Start Redis (required for session management):
   ```bash
   redis-server
   ```

5. Run the app:
   ```bash
   uvicorn app.main:app --reload
   ```

6. Open **http://localhost:8000** in your browser

## UI overview

- **Upload screen** — drag & drop PDF zone, job description textarea, Start Chat button
- **Chat screen** — ChatGPT-style bubbles (user right / AI left), typing indicator, Enter to send
- Single `index.html` file — no frameworks, no build tools
- `session_id` stored in a JS variable only (no localStorage, no cookies)

## Notes

- Do not commit `.env` or `.venv/`
- Redis must be running before starting the server
- The legacy `/analyse/` and `/analyse_text/` endpoints still work but are not exposed in the UI
