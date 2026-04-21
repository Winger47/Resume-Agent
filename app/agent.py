from app.extractor import extract_skills_llm
from app.ai_agent import get_suggestions
from app.matcher import match_skills
from groq import Groq
import os
import json
from dotenv import load_dotenv
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


tools = [
    {
        "type": "function",
        "function": {
            "name": "extract_skills",
            "description": "Extract technical skills from text",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "text to extract skills from"}
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "match_skills",
            "description": "Compare resume skills with JD skills and return score",
            "parameters": {
                "type": "object",
                "properties": {
                    "resume_skills": {"type": "array", "description": "skills from resume"},
                    "jd_skills": {"type": "array", "description": "skills from job description"}
                },
                "required": ["resume_skills", "jd_skills"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_suggestions",
            "description": "Generate improvement suggestions based on missing skills",
            "parameters": {
                "type": "object",
                "properties": {
                    "resume_text": {"type": "string", "description": "full resume text"},
                    "jd_text": {"type": "string", "description": "job description text"},
                    "missing_skills": {"type": "array", "description": "skills missing from resume"}
                },
                "required": ["resume_text", "jd_text", "missing_skills"]
            }
        }
    }
]

def run_agent(resume_text: str, jd_text: str) -> dict:
    tool_map = {
        "extract_skills": extract_skills_llm,
        "match_skills": match_skills,
        "get_suggestions": get_suggestions
    }

    messages = [
        {
            "role": "system",
            "content": """You are a resume analysis agent. Follow these steps exactly using the provided tools:
Step 1: Call extract_skills with the resume text
Step 2: Call extract_skills with the job description text  
Step 3: Call match_skills with resume_skills and jd_skills as lists
Step 4: Call get_suggestions with resume_text, jd_text and missing_skills
Step 5: Return a final summary of the analysis.
Always pass correct types - resume_skills and jd_skills must be arrays."""
        },
        {
            "role": "user",
            "content": f"Resume:\n{resume_text}\n\nJob Description:\n{jd_text}"
        }
    ]

    try:
        while True:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                tools=tools
            )

            message = response.choices[0].message

            if message.tool_calls:
                messages.append(message)
                for tool_call in message.tool_calls:
                    function_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)
                    function_to_call = tool_map[function_name]
                    result = function_to_call(**arguments)
                    messages.append({
                        "role": "tool",
                        "content": str(result),
                        "tool_call_id": tool_call.id
                    })
            else:
                return {"result": message.content}
    except Exception as e:
        return {"error": str(e), "result": "Agent failed — try /analyse/ endpoint instead"}