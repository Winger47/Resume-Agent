from groq import Groq
import os
from dotenv import load_dotenv
import json
load_dotenv() 
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
SKILLS = {
    "python", "fastapi", "django", "flask",
    "docker", "kubernetes", "aws", "gcp", "azure",
    "redis", "rabbitmq", "postgresql", "mysql", "mongodb",
    "react", "nodejs", "javascript", "typescript",
    "git", "ci/cd", "grpc", "kafka",
    "langchain", "chromadb", "numpy", "pandas",
    "celery", "linux", "rest", "graphql"
}
def extract_skills(text: str) -> set:
    extracted_skills = set()
    for skill in SKILLS:
        if skill in text.lower():
            extracted_skills.add(skill)
    return extracted_skills

def extract_skills_llm(text: str) -> set:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": """You are a skill extraction API.
Extract all technical skills from the text.
Return ONLY a valid JSON array of lowercase strings.
No explanation. No categories. No markdown. No bullet points.
Only output the JSON array itself.
Correct output: ["python", "docker", "aws"]
Wrong output: Here are the skills: 1. Python 2. Docker"""},
            {"role": "user", "content": text}
        ]
    )
    result = response.choices[0].message.content.strip()
    try:
        return set(json.loads(result))
    except json.JSONDecodeError:
        # fallback to static extraction if LLM returns wrong format
        return extract_skills(text)

