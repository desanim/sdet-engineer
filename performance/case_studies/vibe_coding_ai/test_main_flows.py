"""
Automated Test Suite for Main Flows (Happy Path) of Vibe-Coding Platform.
Validates: Auth -> SSE Token Streaming (TTFT) -> Sandbox Container Lifecycle -> GitHub Export.
"""
import asyncio
import json
import sys
import time
import httpx

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_URL = "http://127.0.0.1:8088"


async def run_main_flows():
    print("\n" + "=" * 75)
    print(" 🌟 TEST SUITE: VIBE-CODING APP MAIN FLOWS (HAPPY PATH) ")
    print("=" * 75)

    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        # Step 1: Health Check
        print("\n[Step 1] Checking Platform Health Status...")
        res = await client.get("/health")
        assert res.status_code == 200, f"Health check failed: {res.text}"
        print(f" [✓] Health Check OK: {res.json()['service']}")

        # Step 2: Authentication & Initial Credits
        print("\n[Step 2] User Authentication & Credit Verification...")
        login_res = await client.post("/api/v1/auth/login", json={"username": "ph_vibecoder_01"})
        assert login_res.status_code == 200
        auth_data = login_res.json()
        token = auth_data["token"]
        initial_credits = auth_data["credits"]
        print(f" [✓] Authenticated as 'ph_vibecoder_01'. Token: {token[:12]}... | Credits: {initial_credits}")
        headers = {"Authorization": f"Bearer {token}"}

        # Step 3: Server-Sent Events (SSE) AI Code Generation & TTFT Measurement
        print("\n[Step 3] Initiating Real-Time AI Code Generation (SSE Streaming)...")
        prompt_payload = {
            "prompt": "Build an AI habit tracker with streak counter",
            "target_framework": "react-vite",
            "model": "claude-3-7-sonnet"
        }

        stream_start_time = time.time()
        ttft = None
        code_chunks = []

        async with client.stream("POST", "/api/v1/ai/generate-stream", json=prompt_payload, headers=headers) as response:
            assert response.status_code == 200, f"SSE connection failed with {response.status_code}"
            
            async for line in response.aiter_lines():
                if line.startswith("data:"):
                    raw_data = line.replace("data:", "").strip()
                    if not raw_data:
                        continue
                    event_data = json.loads(raw_data)

                    # Capture Time to First Token (TTFT)
                    if "chunk" in event_data:
                        if ttft is None:
                            ttft = time.time() - stream_start_time
                            print(f" [✓] First Token Received! TTFT = {ttft * 1000:.1f}ms (SLA < 500ms: {'PASS' if ttft < 0.5 else 'WARN'})")
                        code_chunks.append(event_data["chunk"])

                    if event_data.get("status") == "completed":
                        remaining_credits = event_data.get("credits_remaining")
                        print(f" [✓] Code Streaming Complete! Remaining Credits: {remaining_credits}")

        total_stream_time = time.time() - stream_start_time
        full_generated_code = "".join(code_chunks)
        print(f" [✓] Assembled {len(full_generated_code)} characters of React code in {total_stream_time:.2f}s.")
        assert "export default function VibeApp()" in full_generated_code, "Generated code structure missing!"

        # Step 4: Sandbox Container Spawn & Preview
        print("\n[Step 4] Spawning Isolated In-Browser Sandbox Container...")
        sandbox_res = await client.post(
            "/api/v1/sandbox/spawn",
            json={"project_name": "habit-tracker-vibe", "code_bundle": full_generated_code},
            headers=headers,
        )
        assert sandbox_res.status_code == 200, f"Sandbox failed: {sandbox_res.text}"
        sandbox_data = sandbox_res.json()
        sandbox_id = sandbox_data["sandbox_id"]
        preview_url = sandbox_data["preview_url"]
        print(f" [✓] Sandbox Ready: {sandbox_id} -> Live Preview: {preview_url}")

        # Step 5: Export to GitHub
        print("\n[Step 5] Exporting Project to GitHub Repository...")
        export_res = await client.post(
            "/api/v1/export/github",
            json={"sandbox_id": sandbox_id, "repository_name": "ai-habit-tracker"},
            headers=headers,
        )
        assert export_res.status_code == 200, f"GitHub export failed: {export_res.text}"
        export_data = export_res.json()
        print(f" [✓] Export Succeeded: {export_data['repository_url']} (Commit SHA: {export_data['commit_sha'][:8]})")

        # Step 6: Final Credits Audit
        print("\n[Step 6] Verifying Final Account State...")
        profile_res = await client.get("/api/v1/user/profile", headers={"Authorization": f"Bearer {token}"})
        assert profile_res.status_code == 200
        current_credits = profile_res.json()["credits"]
        print(f" [✓] Final Credits: {current_credits} (Accurately decremented by 1 from {initial_credits})")
        assert current_credits == initial_credits - 1, "Credit balance mismatch!"

    print("\n" + "=" * 75)
    print(" 🎉 ALL MAIN FLOWS PASSED PERFECTLY! [6/6 STEPS OK] ")
    print("=" * 75)


if __name__ == "__main__":
    asyncio.run(run_main_flows())
