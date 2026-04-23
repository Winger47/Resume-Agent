import redis
import os
from dotenv import load_dotenv
import json
from typing import List
load_dotenv()
r = redis.from_url(os.getenv("REDIS_URL"))

def save_resume(session_id: str, text: str):
    r.set(f"resume:{session_id}", text)

def get_resume(session_id: str) -> str:
    data = r.get(f"resume:{session_id}")
    return data.decode("utf-8") if data else None

def set_history(session_id:str, history:List[str]):
    r.set(f"history:{session_id}", json.dumps(history))

def get_history(session_id:str)->list:
    data=r.get(f"history:{session_id}")

    return json.loads(data.decode("utf-8")) if data else []