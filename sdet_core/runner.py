"""
SDET Performance Test Orchestrator & Runner.
Executes Apache JMeter in Non-GUI mode with dynamic parameter injection and triggers SLA analysis.
"""
import argparse
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime


def find_jmeter_binary(custom_path: str = None) -> str:
    """Detects JMeter executable in custom path, JMETER_HOME, or system PATH."""
    candidates = []
    if custom_path:
        candidates.append(custom_path)

    jmeter_home = os.environ.get("JMETER_HOME")
    if jmeter_home:
        candidates.append(os.path.join(jmeter_home, "bin", "jmeter.bat" if os.name == "nt" else "jmeter"))

    # Check system PATH
    system_jmeter = shutil.which("jmeter.bat" if os.name == "nt" else "jmeter")
    if system_jmeter:
        candidates.append(system_jmeter)

    # Common Windows locations
    if os.name == "nt":
        candidates.extend([
            r"C:\Program Files\apache-jmeter\bin\jmeter.bat",
            r"C:\Tools\apache-jmeter\bin\jmeter.bat",
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\apache-jmeter\bin\jmeter.bat"),
        ])

    for candidate in candidates:
        if candidate and os.path.isfile(candidate):
            return candidate

    return ""


def ensure_test_data(data_path: str, count: int = 500):
    """Ensures test data CSV file exists prior to execution."""
    if not os.path.exists(data_path) or os.path.getsize(data_path) == 0:
        print(f"[!] Test data not found at: {data_path}. Generating {count} records automatically...")
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        generator_script = os.path.join(project_root, "data_generator", "generate_data.py")
        subprocess.run([sys.executable, generator_script, "--count", str(count), "--output", data_path], check=True)


def run_performance_test(
    plan_path: str,
    threads: int = 10,
    rampup: int = 5,
    duration: int = 30,
    host: str = "localhost",
    port: int = 8000,
    protocol: str = "http",
    custom_jmeter: str = None,
    output_base: str = None,
) -> int:
    """Executes JMeter non-gui test plan with injected parameters."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # Resolve paths
    if not os.path.isabs(plan_path):
        plan_path = os.path.join(project_root, plan_path)

    csv_data_path = os.path.join(project_root, "test_data", "users.csv")
    ensure_test_data(csv_data_path, count=max(threads * 10, 200))

    jmeter_bin = find_jmeter_binary(custom_jmeter)
    if not jmeter_bin:
        print("[ERROR] Apache JMeter executable could not be found.")
        print("Please ensure JMeter is installed and added to PATH, or set JMETER_HOME.")
        print("Installation reference: https://jmeter.apache.org/download_jmeter.cgi")
        return 127

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if not output_base:
        output_base = os.path.join(project_root, "reports", f"run_{timestamp}")

    os.makedirs(output_base, exist_ok=True)
    jtl_file = os.path.join(output_base, "results.jtl")
    html_report_dir = os.path.join(output_base, "html_dashboard")
    log_file = os.path.join(output_base, "jmeter.log")

    print("=" * 70)
    print(" 🚀 SDET PERFORMANCE RUNNER: INITIATING LOAD TEST ")
    print("=" * 70)
    print(f" • JMeter Binary   : {jmeter_bin}")
    print(f" • Test Plan       : {plan_path}")
    print(f" • Virtual Users   : {threads} threads")
    print(f" • Ramp-up Period  : {rampup}s")
    print(f" • Test Duration   : {duration}s")
    print(f" • Target Endpoint : {protocol}://{host}:{port}")
    print(f" • Output Artifacts: {output_base}")
    print("=" * 70)

    # Relative or normalized path for CSV in JMeter
    normalized_csv_path = csv_data_path.replace("\\", "/")

    cmd = [
        jmeter_bin,
        "-n",  # Non-GUI mode
        "-t", plan_path,
        "-l", jtl_file,
        "-j", log_file,
        "-e",  # Generate HTML dashboard
        "-o", html_report_dir,
        f"-Jthreads={threads}",
        f"-Jrampup={rampup}",
        f"-Jduration={duration}",
        f"-Jhost={host}",
        f"-Jport={port}",
        f"-Jprotocol={protocol}",
        f"-Jcsv_path={normalized_csv_path}",
    ]

    start_time = time.time()
    try:
        proc = subprocess.run(cmd, check=False)
        execution_time = time.time() - start_time
        print(f"\n[✓] JMeter execution finished in {execution_time:.2f} seconds.")
    except Exception as exc:
        print(f"[!] Execution failed with error: {exc}")
        return 1

    # Automatically trigger SLA Analyzer
    analyzer_script = os.path.join(project_root, "sdet_core", "analyzer.py")
    sla_config = os.path.join(project_root, "config", "sla_config.json")
    print("\n" + "=" * 70)
    print(" 🔍 SDET ANALYZER: EVALUATING QUALITY GATES & SLAs ")
    print("=" * 70)

    analyzer_cmd = [
        sys.executable,
        analyzer_script,
        "--jtl", jtl_file,
        "--sla-config", sla_config,
        "--output-dir", output_base,
    ]
    analyzer_res = subprocess.run(analyzer_cmd)
    return analyzer_res.returncode


def main():
    parser = argparse.ArgumentParser(description="SDET JMeter Non-GUI Performance Runner")
    parser.add_argument("--plan", default="jmeter_plans/ecommerce_performance_test.jmx", help="Path to .jmx test plan")
    parser.add_argument("--threads", type=int, default=10, help="Number of virtual users (threads)")
    parser.add_argument("--rampup", type=int, default=5, help="Ramp-up time in seconds")
    parser.add_argument("--duration", type=int, default=20, help="Test duration in seconds")
    parser.add_argument("--host", default="localhost", help="Target API host")
    parser.add_argument("--port", type=int, default=8000, help="Target API port")
    parser.add_argument("--protocol", default="http", help="Target protocol (http/https)")
    parser.add_argument("--jmeter-bin", default=None, help="Explicit path to jmeter executable")
    parser.add_argument("--output-dir", default=None, help="Custom output directory")

    args = parser.parse_args()
    exit_code = run_performance_test(
        plan_path=args.plan,
        threads=args.threads,
        rampup=args.rampup,
        duration=args.duration,
        host=args.host,
        port=args.port,
        protocol=args.protocol,
        custom_jmeter=args.jmeter_bin,
        output_base=args.output_dir,
    )
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
