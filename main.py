from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os, requests

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static HTML
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
def home():
    return FileResponse("static/index.html")

# NewsAPI route
class Topic(BaseModel):
    title: str
    summary: str
    reason_trending: str
    source_link: str

@app.get("/get-topics", response_model=List[Topic])
def get_trending_topics(niche: str = Query(...)):
    from_date = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
    to_date = datetime.today().strftime('%Y-%m-%d')

    url = f"https://newsapi.org/v2/everything?q={niche}&from={from_date}&to={to_date}&sortBy=popularity&pageSize=10&apiKey={NEWS_API_KEY}"

    response = requests.get(url)
    data = response.json()

    if data.get("status") != "ok":
        return []

    return [
        Topic(
            title=article["title"],
            summary=article["description"] or "No summary available.",
            reason_trending=f"Published by {article['source']['name']} on {article['publishedAt'][:10]}",
            source_link=article["url"]
        )
        for article in data.get("articles", [])
    ]
