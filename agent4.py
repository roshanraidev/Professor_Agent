from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)
app = FastAPI()

# Enable CORS so it can talk to your HTML/JS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class BlogRequest(BaseModel):
    blog: str

@app.post("/humanize-blog")
async def humanize_blog(request: BlogRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional editor. Your job is to rewrite blogs to sound more natural, structured, "
                        "and engaging. Structure the blog into: introduction, clear subheadings, body content, analysis, "
                        "comparison (if relevant), and conclusion. Make it human-like, reader-friendly, and professional. "
                        "Add headings where helpful."
                    )
                },
                {
                    "role": "user",
                    "content": request.blog
                }
            ],
            temperature=0.7
        )
        rewritten = response.choices[0].message.content
        return {"success": True, "result": rewritten}
    except Exception as e:
        return {"success": False, "error": str(e)}
