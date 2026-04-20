from fastapi import FastAPI, Form, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import io
from app.matcher import match_skills
from app.extractor import  extract_skills_llm
from app.ai_agent import get_suggestions
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

@app.get("/health")
def health():
    return {"status": "ok"}

# @app.get("/")
# def root():
#     return {"message": "Resume Analyzer"}