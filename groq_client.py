import os
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def analyze_resume_with_groq(resume_text, job_description):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"Compare this resume with the job description and give a detailed analysis:\n\nResume:\n{resume_text}\n\nJob Description:\n{job_description}"

    body = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "llama3-8b-8192"

    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=body)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error from Groq API: {response.text}"