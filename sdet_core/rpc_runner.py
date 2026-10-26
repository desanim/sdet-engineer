"""
Blockchain / Web3 SDET Load Test Orchestrator.
Executes Apache JMeter in Non-GUI mode against EVM JSON-RPC nodes with dynamic parameters.
"""
import argparse
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def find_jmeter_binary(custom_path: str = None) -> str:
    """Locates JMeter binary from custom path, JMETER_HOME, or system PATH."""
    candidates = []
    if custom_path:
        candidates.append(custom_path)

    jmeter_home = os.environ.get("JMETER_HOME")
    if jmeter_home:
        candidates.append(os.path.join(jmeter_home, "bin", "jmeter.bat" if os.name == "nt" else "jmeter"))

    system_jmeter = shutil.which("jmeter.bat" if os.name == "nt" else "jmeter")
    if system_jmeter:
        candidates.append(system_jmeter)

    if os.name == "nt":
        candidates.extend([
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\apache-jmeter\bin\jmeter.bat"),
            r"C:\Program Files\apache-jmeter\bin\jmeter.bat",
            r"C:\Tools\apache-jmeter\bin\jmeter.bat",
        ])

    for candidate in candidates:
        if candidate and os.path.isfile(candidate):
            return candidate

    return ""


def ensure_wallet_dataset(wallet_csv_path: str, count: int = 500):
    """Generates synthetic Web3 wallet keypairs if CSV is missing."""
    if not os.path.exists(wallet_csv_path) or os.path.getsize(wallet_csv_path) == 0:
        print(f"[*] Wallet dataset missing at {wallet_csv_path}. Generating {count} accounts...")
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        gen_script = os.path.join(project_root, "wallet_generator", "generate_wallets.py")
        subprocess.run([sys.executable, gen_script, "--count", str(count), "--output", wallet_csv_path], check=True)


def run_blockchain_load_test(
    plan_path: str,
    threads: int = 20,
    rampup: int = 5,
    duration: int = 30,
    host: str = "localhost",
    port: int = 8545,
    protocol: str = "http",
    custom_jmeter: str = None,
    output_base: str = None,
) -> int:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    if not os.path.isabs(plan_path):
        plan_path = os.path.join(project_root, plan_path)

    wallet_csv = os.path.join(project_root, "test_data", "wallets.csv")
    ensure_wallet_dataset(wallet_csv, count=max(threads * 20, 200))

    jmeter_bin = find_jmeter_binary(custom_jmeter)
    if not jmeter_bin:
        print("[!] Apache JMeter not found in PATH or standard directories.")
        print("[*] To install: download from https://jmeter.apache.org/download_jmeter.cgi")
        return 127

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if not output_base:
        output_base = os.path.join(project_root, "reports", f"rpc_run_{timestamp}")

    os.makedirs(output_base, exist_ok=True)
    jtl_file = os.path.join(output_base, "rpc_results.jtl")
    html_dashboard = os.path.join(output_base, "html_dashboard")
    log_file = os.path.join(output_base, "jmeter.log")

    normalized_csv_path = wallet_csv.replace("\\", "/")

    print("\n" + "=" * 80)
    print(" ⛓️  BLOCKCHAIN SDET RUNNER: EVM JSON-RPC BENCHMARK ")
    print("=" * 80)
    print(f" • RPC Endpoint    : {protocol}://{host}:{port}")
    print(f" • Virtual Traders : {threads} concurrent threads")
    print(f" • Ramp-up         : {rampup}s")
    print(f" • Duration        : {duration}s")
    print(f" • Test Plan       : {plan_path}")
    print(f" • Output Directory: {output_base}")
    print("=" * 80 + "\n")

    cmd = [
        jmeter_bin,
        "-n",
        "-t", plan_path,
        "-l", jtl_file,
        "-j", log_file,
        "-e",
        "-o", html_dashboard,
        f"-Jthreads={threads}",
        f"-Jrampup={rampup}",
        f"-Jduration={duration}",
        f"-Jhost={host}",
        f"-Jport={port}",
        f"-Jprotocol={protocol}",
        f"-Jcsv_path={normalized_csv_path}",
    ]

    t0 = time.time()
    try:
        subprocess.run(cmd, check=False)
        elapsed = time.time() - t0
        print(f"\n[✓] JMeter RPC execution finished in {elapsed:.2f}s.")
    except Exception as exc:
        print(f"[!] JMeter execution error: {exc}")
        return 1

    # Trigger Blockchain Quality Gate Analyzer
    analyzer_script = os.path.join(project_root, "sdet_core", "web3_analyzer.py")
    sla_config = os.path.join(project_root, "config", "web3_sla_config.json")

    analyzer_cmd = [
        sys.executable,
        analyzer_script,
        "--jtl", jtl_file,
        "--sla-config", sla_config,
        "--output-dir", output_base,
    ]
    res = subprocess.run(analyzer_cmd)
    return res.returncode


def main():
    parser = argparse.ArgumentParser(description="Blockchain EVM RPC Load Test Orchestrator")
    parser.add_argument("--plan", default="jmeter_plans/blockchain_tps_benchmark.jmx", help="JMeter .jmx plan")
    parser.add_argument("--threads", type=int, default=20, help="Concurrent RPC client threads")
    parser.add_argument("--rampup", type=int, default=5, help="Ramp up in seconds")
    parser.add_argument("--duration", type=int, default=30, help="Test duration in seconds")
    parser.add_argument("--host", default="localhost", help="RPC Host")
    parser.add_argument("--port", type=int, default=8545, help="RPC Port")
    parser.add_argument("--output-dir", default=None, help="Output directory")

    args = parser.parse_args()
    code = run_blockchain_load_test(
        plan_path=args.plan,
        threads=args.threads,
        rampup=args.rampup,
        duration=args.duration,
        host=args.host,
        port=args.port,
        output_base=args.output_dir,
    )
    sys.exit(code)


if __name__ == "__main__":
    main()
