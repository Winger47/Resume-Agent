from groq import Groq
import os
from dotenv import load_dotenv
from app.session_manager import get_resume, get_jd, get_history, save_history

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def chat(session_id: str, user_message: str) -> str:
    resume_text = get_resume(session_id)
    jd_text = get_jd(session_id)
    history = get_history(session_id)

    messages = [
        {
            "role": "system",
            "content": """You are an expert resume coach for top product-based companies and startups.
You have already analyzed the user's resume against a job description.
Your role is to:
- Answer questions about the analysis
- Suggest what to add, remove or improve in the resume
- Help rewrite specific sections on request
- Give honest, direct feedback like a senior engineer would
Always be specific and actionable. Never give vague advice."""
        },
        {
            "role": "user",
            "content": f"Here is my resume:\n{resume_text}\n\nHere is the job description:\n{jd_text}"
        }
    ] + history + [
        {"role": "user", "content": user_message}
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    reply = response.choices[0].message.content

    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": reply})
    save_history(session_id, history)

    return reply