from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from openai import OpenAI  # updated import

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)  # initialize client

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BlogInput(BaseModel):
    title: str
    summary: str
    reason_trending: str
    source_link: str
    length: str
    tone: str

@app.post("/generate-blog")
def generate_blog(data: BlogInput):
    length_instruction = {
        "short": "Write a short blog post around 150 words.",
        "medium": "Write a standard blog post around 400–500 words.",
        "long": "Write a detailed blog post around 800–1000 words."
    }.get(data.length, "Write a blog post.")

    tone_instruction = f"Use a {data.tone} tone."

    prompt = f"""
{length_instruction}
{tone_instruction}

Title: {data.title}
Summary: {data.summary}
Trending Because: {data.reason_trending}
Source: {data.source_link}

Structure it with:
- An engaging introduction
- 2–3 informative subheadings
- A clear and strong conclusion
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return {"success": True, "blog": response.choices[0].message.content}
    except Exception as e:
        return {"success": False, "error": str(e)}
