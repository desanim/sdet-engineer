"""
Master CLI: Vibe-App MVP Launch-Readiness & Security Auditor.
Executes 4 comprehensive audit modules against any target MVP URL:
1. Secrets & Credentials Leak Scan
2. Product Hunt 50-User Burst Spike Test
3. React Crashes & Broken Asset Crawl
4. Mobile Viewport & OpenGraph Social Meta Check
"""
import argparse
import asyncio
import json
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

from scanners.error_boundary_crawler import crawl_and_audit_errors
from scanners.mobile_ux_gate import audit_mobile_and_meta
from scanners.secrets_scanner import scan_url_for_secrets
from scanners.spike_load_tester import run_spike_test


def calculate_overall_grade(secrets: dict, spike: dict, crawler: dict, mobile: dict) -> tuple:
    critical_leaks = secrets.get("critical_leaks", 0)
    ui_crashes = crawler.get("ui_crashes_found", 0)
    err_5xx_rate = spike.get("error_5xx_rate_pct", 0.0)
    p95 = spike.get("latency_p95_ms", 0.0)

    # Hard Blockers -> Grade F
    if critical_leaks > 0 or ui_crashes > 0 or err_5xx_rate > 10.0:
        return "F", "🔴 DO NOT LAUNCH (Critical Security Leak or Severe Instability)"

    # Warnings -> Grade C
    if len(secrets.get("findings", [])) > 0 or err_5xx_rate > 3.0 or p95 > 2500.0:
        return "C", "🟠 HIGH RISK (High Latency or Asset Failures)"

    # Minor issues -> Grade B
    if crawler.get("broken_assets_found", 0) > 0 or len(mobile.get("findings", [])) > 0:
        return "B", "🟡 LAUNCH WITH CAUTION (Minor UX / Broken Assets)"

    return "A", "🟢 LAUNCH READY (Production Grade & Resilient)"


async def run_full_audit(target_url: str, output_dir: str) -> int:
    print("\n" + "=" * 85)
    print(" 🚀 VIBE-APP MVP LAUNCH-READINESS & SECURITY AUDIT ENGINE ")
    print("=" * 85)
    print(f" • Target MVP URL   : {target_url}")
    print(f" • Audit Scope      : Client Secrets | Traffic Spike | UI Crashes | Mobile UX")
    print("=" * 85 + "\n")

    # Module 1: Secrets Scan
    print("[1/4] Scanning HTML & JavaScript Bundles for Exposed API Keys...")
    secrets_res = await scan_url_for_secrets(target_url)
    leak_count = secrets_res.get("leak_count", 0)
    print(f" -> Found {leak_count} secret exposure(s) across {secrets_res.get('assets_scanned', 1)} asset(s).")
    for f in secrets_res.get("findings", []):
        print(f"    • [{f['severity']}] {f['secret_type']} ({f['masked_value']}) in {f.get('source')}")

    # Module 2: Spike Load Test
    print("\n[2/4] Executing 50-User Burst Traffic Spike Test (Product Hunt Simulation)...")
    spike_res = await run_spike_test(target_url, virtual_users=30, burst_duration_sec=5)
    print(f" -> Dispatched {spike_res['total_requests']} requests | Throughput: {spike_res['throughput_rps']} RPS")
    print(f" -> Latency p50: {spike_res['latency_p50_ms']}ms | p95: {spike_res['latency_p95_ms']}ms | 5xx Errors: {spike_res['error_5xx_rate_pct']}%")

    # Module 3: Error Boundary & Asset Crawl
    print("\n[3/4] Crawling for Unhandled React Crashes & Broken Assets...")
    crawl_res = await crawl_and_audit_errors(target_url)
    print(f" -> UI Crashes Detected : {crawl_res.get('ui_crashes_found', 0)}")
    print(f" -> Broken Image Assets : {crawl_res.get('broken_assets_found', 0)}")

    # Module 4: Mobile & Meta Gate
    print("\n[4/4] Verifying Mobile Viewport & OpenGraph Viral Sharing Meta...")
    mobile_res = await audit_mobile_and_meta(target_url)
    print(f" -> Passed Checks : {mobile_res.get('passed_checks', 0)}")
    print(f" -> Detected Issues: {mobile_res.get('issues_count', 0)}")

    # Score Calculation
    grade, verdict = calculate_overall_grade(secrets_res, spike_res, crawl_res, mobile_res)

    print("\n" + "=" * 85)
    print(" 📊 VIBE-CODED MVP LAUNCH-READINESS SCORECARD ")
    print("=" * 85)
    print(f" OVERALL GRADE     : [ {grade} ]")
    print(f" VERDICT           : {verdict}")
    print("-" * 85)
    print(f" • Leaked Credentials        : {leak_count} issues ({secrets_res.get('critical_leaks', 0)} Critical)")
    print(f" • Spike Latency (p95)       : {spike_res['latency_p95_ms']}ms (5xx Error Rate: {spike_res['error_5xx_rate_pct']}%)")
    print(f" • Broken Images / Assets    : {crawl_res.get('broken_assets_found', 0)} broken links")
    print(f" • Mobile & OpenGraph Meta   : {'Optimized' if mobile_res.get('issues_count', 0) == 0 else 'Missing Social Cards'}")
    print("=" * 85 + "\n")

    # Export Reports
    os.makedirs(output_dir, exist_ok=True)
    full_report = {
        "target_url": target_url,
        "grade": grade,
        "verdict": verdict,
        "timestamp": time.time(),
        "modules": {
            "secrets_scan": secrets_res,
            "spike_load_test": spike_res,
            "error_crawler": crawl_res,
            "mobile_ux": mobile_res,
        },
    }

    json_path = os.path.join(output_dir, "launch_readiness_audit.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(full_report, f, indent=2)

    md_path = os.path.join(output_dir, "launch_readiness_audit.md")
    generate_markdown_report(full_report, md_path)

    print(f"[+] Saved JSON Audit Report to: {json_path}")
    print(f"[+] Saved Markdown Report to   : {md_path}\n")

    return 0 if grade in ("A", "B") else 1


def generate_markdown_report(report: dict, md_path: str):
    grade = report["grade"]
    verdict = report["verdict"]
    sec = report["modules"]["secrets_scan"]
    spk = report["modules"]["spike_load_test"]
    crw = report["modules"]["error_crawler"]
    mob = report["modules"]["mobile_ux"]

    lines = [
        f"# 🚀 Vibe-App MVP Launch-Readiness Audit Report\n",
        f"**Target Application**: `{report['target_url']}`  ",
        f"**Overall Launch Grade**: `[ {grade} ]` — **{verdict}**\n",
        "## Executive Summary Scorecard\n",
        "| Audit Module | Key Result | Status |",
        "| :--- | :--- | :--- |",
        f"| **1. Client Secrets Scanner** | Found `{sec.get('leak_count', 0)}` exposed keys (`{sec.get('critical_leaks', 0)}` Critical) | {'❌ FAIL' if sec.get('critical_leaks', 0) > 0 else '✅ PASS'} |",
        f"| **2. Traffic Spike Test (50 VUs)** | Throughput `{spk.get('throughput_rps', 0)}` RPS, p95 `{spk.get('latency_p95_ms', 0)}`ms, 5xx Rate `{spk.get('error_5xx_rate_pct', 0)}`% | {'✅ PASS' if spk.get('launch_ready') else '❌ FAIL'} |",
        f"| **3. UI Crash & Broken Assets** | `{crw.get('ui_crashes_found', 0)}` fatal crashes, `{crw.get('broken_assets_found', 0)}` broken images | {'❌ FAIL' if crw.get('ui_crashes_found', 0) > 0 else '⚠️ WARNING'} |",
        f"| **4. Mobile & Social Meta** | `{mob.get('passed_checks', 0)}` passed checks, `{mob.get('issues_count', 0)}` warnings | {'✅ PASS' if mob.get('issues_count', 0) == 0 else '⚠️ WARNING'} |\n",
    ]

    if sec.get("findings"):
        lines.append("### 🔴 Critical Security Vulnerabilities (Immediate Action Required)\n")
        for f in sec["findings"]:
            lines.append(f"- **{f['secret_type']}** detected in `{f.get('source')}`")
            lines.append(f"  - **Value**: `{f['masked_value']}`")
            lines.append(f"  - **Impact**: {f['impact']}")
            lines.append(f"  - **Fix**: {f['remediation']}\n")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def wait_for_server(url: str, timeout: int = 10) -> bool:
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with urllib.request.urlopen(url, timeout=1) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            time.sleep(0.5)
    return False


def main():
    parser = argparse.ArgumentParser(description="Vibe-App MVP Launch-Readiness & Security Auditor")
    parser.add_argument("--target-url", default="http://127.0.0.1:8888", help="Target MVP URL")
    parser.add_argument("--run-mock", action="store_true", default=True, help="Automatically run mock Vibe MVP server")
    parser.add_argument(
        "--output-dir",
        default=os.path.join(os.path.dirname(__file__), "reports"),
        help="Report export directory",
    )

    args = parser.parse_args()

    # If auditing local mock, boot mock server in background
    if args.run_mock and ("127.0.0.1:8888" in args.target_url or "localhost:8888" in args.target_url):
        mock_dir = os.path.join(os.path.dirname(__file__), "mock_target_mvp")
        app_script = os.path.join(mock_dir, "app.py")
        print("[*] Automatically booting Mock Target MVP on http://127.0.0.1:8888...")
        proc = subprocess.Popen(
            [sys.executable, app_script],
            cwd=mock_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        try:
            if not wait_for_server("http://127.0.0.1:8888/health"):
                print("[!] Failed to connect to mock MVP server.")
                return 1
            exit_code = asyncio.run(run_full_audit(args.target_url, args.output_dir))
            return exit_code
        finally:
            print("[*] Tearing down Mock MVP Server...")
            proc.terminate()
            try:
                proc.wait(timeout=2)
            except Exception:
                proc.kill()
    else:
        return asyncio.run(run_full_audit(args.target_url, args.output_dir))


if __name__ == "__main__":
    sys.exit(main())
