"""
Master Orchestrator for Vibe-Coding AI Case Study.
Launches the mock streaming server, executes both Happy Path and Edge Case suites,
and produces a consolidated SDET report.
"""
import os
import subprocess
import sys
import time
import urllib.request

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def wait_for_server(url: str, timeout: int = 15) -> bool:
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with urllib.request.urlopen(url, timeout=1) as response:
                if response.status == 200:
                    return True
        except Exception:
            time.sleep(0.5)
    return False


def main():
    case_study_dir = os.path.dirname(os.path.abspath(__file__))
    server_script = os.path.join(case_study_dir, "mock_vibe_server.py")
    main_tests_script = os.path.join(case_study_dir, "test_main_flows.py")
    edge_tests_script = os.path.join(case_study_dir, "test_edge_and_race_conditions.py")

    print("\n" + "=" * 80)
    print(" 🚀 SDET CASE STUDY: VIBE-CODING AI PLATFORM (PRODUCT HUNT LAUNCH) ")
    print("=" * 80)
    print(" [1/3] Spinning up Mock Vibe Streaming Server on port 8088...")

    server_process = subprocess.Popen(
        [sys.executable, server_script],
        cwd=case_study_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        if not wait_for_server("http://127.0.0.1:8088/health"):
            print("[ERROR] Mock server failed to become healthy within 15 seconds.")
            return 1

        print(" [✓] Mock Server is healthy and listening at http://127.0.0.1:8088\n")

        # Run Suite 1: Happy Path
        print(" [2/3] Executing Main Flows (Happy Path)...")
        main_exit = subprocess.run([sys.executable, main_tests_script]).returncode

        # Run Suite 2: Edge Cases & Concurrency
        print("\n [3/3] Executing Edge Cases & Race Condition Attacks...")
        edge_exit = subprocess.run([sys.executable, edge_tests_script]).returncode

        print("\n" + "=" * 80)
        print(" 📊 CONSOLIDATED CASE STUDY AUDIT RESULT ")
        print("=" * 80)
        print(f" • Main Flows (SSE Streaming, Sandbox, GitHub Export) : {'PASSED (6/6)' if main_exit == 0 else 'FAILED'}")
        print(f" • Edge Cases (Race Conditions, Injections, Timeouts)   : {'PASSED (5/5)' if edge_exit == 0 else 'FAILED'}")
        print("=" * 80)

        overall_status = 0 if (main_exit == 0 and edge_exit == 0) else 1
        if overall_status == 0:
            print("\n [🏆] VERDICT: Production-Ready! All functional, security & concurrency tests passed.\n")
        else:
            print("\n [❌] VERDICT: Quality Gate failed. Please review errors above.\n")

        return overall_status

    finally:
        print("[*] Tearing down Mock Vibe Server...")
        server_process.terminate()
        try:
            server_process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            server_process.kill()


if __name__ == "__main__":
    sys.exit(main())
