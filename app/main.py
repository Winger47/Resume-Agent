from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import io
import uuid
from app.matcher import match_skills
from app.extractor import extract_skills_llm
from app.ai_agent import get_suggestions
from app.agent import run_agent
from app.session_manager import save_resume, save_jd
from app.chat_agent import chat
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def serve_ui():
    return FileResponse("index.html")

@app.post("/analyse/")
async def analyse(file: UploadFile = File(...), jd_text: str = Form(...)):
    content = await file.read()
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
    resume_skills = extract_skills_llm(text)
    jd_skills = extract_skills_llm(jd_text)
    match_result = match_skills(resume_skills, jd_skills)
    suggestions = get_suggestions(text, jd_text, match_result["missing"])
    return {
        "score": match_result["score"],
        "matched_skills": match_result["matched"],
        "missing_skills": match_result["missing"],
        "suggestions": suggestions
    }

@app.post("/analyse_text/")
async def analyse1(file: UploadFile = File(...), jd_text: str = Form(...)):
    content = await file.read()
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
    return run_agent(text, jd_text)

@app.post("/chat/start")
async def start_chat(file: UploadFile = File(...), jd_text: str = Form(...)):
    content = await file.read()
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
    
    session_id = str(uuid.uuid4())
    save_resume(session_id, text)
    
    # debug
    from app.session_manager import get_resume
    check = get_resume(session_id)
    print(f"DEBUG saved and retrieved: {check[:50] if check else 'NONE'}")
    
    save_jd(session_id, jd_text)
    return {"session_id": session_id}
@app.post("/chat/message")
async def chat_message(session_id: str = Form(...), message: str = Form(...)):
    from app.session_manager import get_resume
    resume = get_resume(session_id)
    print(f"DEBUG resume: {resume[:100] if resume else 'NONE'}")  # ← add this
    result = chat(session_id, message)
    return {"response": result}
@app.get("/health")
def health():
    return {"status": "ok"}