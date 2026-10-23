"""
Mock Vibe-Coding AI Platform (FastAPI).
Simulates realistic LLM Server-Sent Events (SSE) streaming,
credit consumption with race-condition protection, and sandbox container lifecycle.
"""
import asyncio
import json
import random
import time
import uuid
from typing import Dict, Optional

from fastapi import FastAPI, Header, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI(
    title="VibeDev AI - Mock Product Hunt Platform",
    description="Backend engine simulating real-time AI code generation, SSE streaming, and sandbox runners.",
    version="2.0.0",
)

# In-memory database
USERS_DB: Dict[str, dict] = {
    "vibe_user_01": {
        "token": "vibe_token_alpha_123",
        "email": "creator@producthunt.com",
        "credits": 3,  # Limited credits for testing race conditions
        "tier": "free",
    }
}
ACTIVE_SANDBOXES: Dict[str, dict] = {}

# Mutex lock for atomic credit transactions (protecting against race condition)
credit_lock = asyncio.Lock()


class LoginRequest(BaseModel):
    username: str


class GenerateCodeRequest(BaseModel):
    prompt: str
    target_framework: Optional[str] = "react-vite"
    model: Optional[str] = "claude-3-7-sonnet"


class SandboxSpawnRequest(BaseModel):
    project_name: str
    code_bundle: str


class ExportGitHubRequest(BaseModel):
    sandbox_id: str
    repository_name: str


def get_authenticated_user(authorization: Optional[str] = Header(None)) -> dict:
    """Helper to validate Bearer token and return user data."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or malformed Authorization header",
        )
    token = authorization.split("Bearer ")[1].strip()
    for user_id, user_data in USERS_DB.items():
        if user_data["token"] == token:
            return {"user_id": user_id, **user_data}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired access token",
    )


@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "healthy", "service": "VibeDev AI Core", "timestamp": time.time()}


@app.post("/api/v1/auth/login", tags=["Auth"])
async def login(req: LoginRequest):
    """Authenticate and grant initial 3 credits."""
    user_id = req.username
    if user_id not in USERS_DB:
        USERS_DB[user_id] = {
            "token": f"vibe_token_{uuid.uuid4().hex[:12]}",
            "email": f"{user_id}@vibe.ai",
            "credits": 3,
            "tier": "free",
        }
    return {
        "user_id": user_id,
        "token": USERS_DB[user_id]["token"],
        "credits": USERS_DB[user_id]["credits"],
    }


@app.get("/api/v1/user/profile", tags=["User"])
async def get_user_profile(authorization: Optional[str] = Header(None)):
    auth_user = get_authenticated_user(authorization)
    current_data = USERS_DB[auth_user["user_id"]]
    return {
        "user_id": auth_user["user_id"],
        "credits": current_data["credits"],
        "tier": current_data["tier"],
    }


@app.post("/api/v1/ai/generate-stream", tags=["AI Streaming"])
async def generate_code_stream(
    req: GenerateCodeRequest,
    authorization: Optional[str] = Header(None),
    simulate_race_bug: bool = Query(False, description="Enable un-locked state to demonstrate race condition"),
):
    """
    Core Vibe-Coding Stream:
    1. Validates & atomically decrements credits.
    2. Streams Server-Sent Events (SSE) code chunks to client.
    """
    auth_user = get_authenticated_user(authorization)
    user_id = auth_user["user_id"]

    # Security check: Prompt Injection / Malicious command filter (Edge Case)
    prohibited_keywords = ["rm -rf", "drop database", "process.env", "eval(", "/etc/shadow"]
    if any(keyword in req.prompt.lower() for keyword in prohibited_keywords):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Prompt rejected: Detected potentially unsafe or malicious code execution directive.",
        )

    # Atomic credit deduction
    if simulate_race_bug:
        # VULNERABLE PATH (simulates common junior developer mistake)
        current_credits = USERS_DB[user_id]["credits"]
        await asyncio.sleep(0.05)  # Window for race condition
        if current_credits <= 0:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="Out of credits! Please upgrade to Pro on Product Hunt.",
            )
        USERS_DB[user_id]["credits"] = current_credits - 1
    else:
        # SECURE PATH (Uses Mutex Lock to guarantee atomic transaction)
        async with credit_lock:
            if USERS_DB[user_id]["credits"] <= 0:
                raise HTTPException(
                    status_code=status.HTTP_402_PAYMENT_REQUIRED,
                    detail="Out of credits! Please upgrade to Pro on Product Hunt.",
                )
            USERS_DB[user_id]["credits"] -= 1

    # Realistic SSE Generator simulating LLM Token Streaming
    async def sse_event_generator():
        yield f"event: start\ndata: {json.dumps({'message': 'Generating project scaffold...', 'timestamp': time.time()})}\n\n"
        
        # Simulate Time to First Token (TTFT: 80ms - 150ms)
        await asyncio.sleep(random.uniform(0.08, 0.15))

        chunks = [
            "// Vibe-Coded Component: Auto-generated\n",
            "import React, { useState } from 'react';\n",
            "import { Button } from '@/components/ui/button';\n\n",
            "export default function VibeApp() {\n",
            "  const [count, setCount] = useState(0);\n",
            "  return (\n",
            "    <div className='p-8 max-w-xl mx-auto shadow-xl rounded-2xl'>\n",
            f"      <h1 className='text-3xl font-bold'>{req.prompt}</h1>\n",
            "      <p className='text-slate-600 mt-2'>Built with Vibe Coding Engine</p>\n",
            "      <Button onClick={() => setCount(c => c + 1)}>Vibes: {count}</Button>\n",
            "    </div>\n",
            "  );\n",
            "}\n",
        ]

        for chunk in chunks:
            await asyncio.sleep(random.uniform(0.02, 0.06))
            payload = {"chunk": chunk, "timestamp": time.time()}
            yield f"event: chunk\ndata: {json.dumps(payload)}\n\n"

        remaining = USERS_DB[user_id]["credits"]
        yield f"event: done\ndata: {json.dumps({'status': 'completed', 'tokens': 168, 'credits_remaining': remaining})}\n\n"

    return StreamingResponse(sse_event_generator(), media_type="text/event-stream")


@app.post("/api/v1/sandbox/spawn", tags=["Sandbox"])
async def spawn_sandbox(req: SandboxSpawnRequest, authorization: Optional[str] = Header(None)):
    """Spawns an isolated in-browser container/sandbox for live preview."""
    get_authenticated_user(authorization)

    # Edge Case: Detect infinite loop simulation in code
    if "while(true)" in req.code_bundle or "while (true)" in req.code_bundle:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="Sandbox compilation failed: Detected infinite execution loop.",
        )

    # Simulate container spin-up cold start (100ms - 250ms)
    await asyncio.sleep(random.uniform(0.10, 0.25))

    sandbox_id = f"box_{uuid.uuid4().hex[:8]}"
    preview_url = f"https://preview-{sandbox_id}.vibeapp.dev"

    ACTIVE_SANDBOXES[sandbox_id] = {
        "id": sandbox_id,
        "project_name": req.project_name,
        "status": "RUNNING",
        "url": preview_url,
        "created_at": time.time(),
    }

    return {
        "sandbox_id": sandbox_id,
        "preview_url": preview_url,
        "status": "READY",
        "cold_start_ms": 150,
    }


@app.post("/api/v1/export/github", tags=["Export"])
async def export_to_github(req: ExportGitHubRequest, authorization: Optional[str] = Header(None)):
    """Export generated project directly to a user's GitHub repo."""
    get_authenticated_user(authorization)

    if req.sandbox_id not in ACTIVE_SANDBOXES:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sandbox {req.sandbox_id} does not exist or has already been terminated.",
        )

    # Simulate GitHub API git tree & commit push (120ms - 220ms)
    await asyncio.sleep(random.uniform(0.12, 0.22))

    return {
        "success": True,
        "repository_url": f"https://github.com/desanim/{req.repository_name}",
        "commit_sha": uuid.uuid4().hex,
        "deployed_vercel": True,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8088)
