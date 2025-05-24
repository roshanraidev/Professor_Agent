from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BlogInput(BaseModel):
    blog: str

@app.post("/improve-blog")
def improve_blog(data: BlogInput):
    prompt = f"""
You are an SEO expert and fact-checker.

1. Improve the blog post for SEO (keywords, structure, clarity).
2. Add a 160-character meta description.
3. Fact-check any major claims and suggest corrections if needed.

Respond in this format:
---
Improved Blog:
[Improved version]

Meta Description:
[Short SEO meta description]

Corrections (if any):
[List with explanation or 'None']
---
    
Blog:
{data.blog}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6
        )
        return {"success": True, "result": response.choices[0].message.content}
    except Exception as e:
        return {"success": False, "error": str(e)}
