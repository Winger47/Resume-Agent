from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv() 
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_suggestions(resume_text: str, jd_text: str, missing_skills: list):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # ← replace llama3-8b-8192 with this
        messages=[
            {
                "role": "system",
                "content": """You are an expert resume coach and ATS specialist.
Analyze the resume against the job description and return exactly 5 specific, actionable suggestions.

Rules:
- Focus on the missing skills first
- Each suggestion must start with an action verb (Add, Highlight, Include, Quantify, Mention)
- Be specific, not vague. Bad: 'improve your resume'. Good: 'Add a Kubernetes project to your experience section'
- Return as a numbered list, nothing else. No intro, no conclusion."""
            },
            {
                "role": "user",
                "content": f"""Resume:
{resume_text}

Job Description:
{jd_text}

Missing Skills:
{', '.join(missing_skills)}

Give me 5 specific suggestions to improve my resume for this job."""
            }
        ]
    )
    return response.choices[0].message.content

