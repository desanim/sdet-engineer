"""
Realistic Mock Vibe-Coded MVP Web App (FastAPI).
Serves landing page with intentional realistic vulnerabilities for SDET Audit Engine testing.
"""
import asyncio
import os
import random
import time
import uuid

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="VibeResume AI - Sample Vibe-Coded MVP")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=HTMLResponse)
async def landing_page():
    html_file = os.path.join(TEMPLATES_DIR, "index.html")
    with open(html_file, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/health")
async def health():
    return {"status": "ok", "app": "VibeResume AI", "timestamp": time.time()}


@app.get("/api/generate")
async def generate_resume_api():
    # Simulate LLM pipeline latency (40ms - 90ms)
    await asyncio.sleep(random.uniform(0.04, 0.09))
    return {
        "status": "SUCCESS",
        "id": f"res_{uuid.uuid4().hex[:8]}",
        "ats_score": 96,
        "created_at": time.time(),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8888, log_level="warning")
