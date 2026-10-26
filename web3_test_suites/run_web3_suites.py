"""
Master Orchestrator for Web3 & Blockchain SDET Test Suites.
Launches the mock EVM JSON-RPC node, runs DEX concurrency and nonce collision suites,
and produces a consolidated blockchain audit report.
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


def wait_for_node(url: str, timeout: int = 15) -> bool:
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
    suites_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(suites_dir, ".."))
    node_script = os.path.join(project_root, "mock_rpc_node", "app.py")
    dex_script = os.path.join(suites_dir, "test_dex_swap_concurrency.py")
    nonce_script = os.path.join(suites_dir, "test_nonce_race_condition.py")

    print("\n" + "=" * 80)
    print(" ⛓️  WEB3 SDET TEST SUITE: EVM CONCURRENCY & MEMPOOL VALIDATION ")
    print("=" * 80)
    print(" [1/3] Spinning up Mock EVM JSON-RPC Node on port 8545...")

    node_process = subprocess.Popen(
        [sys.executable, node_script],
        cwd=os.path.join(project_root, "mock_rpc_node"),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        if not wait_for_node("http://127.0.0.1:8545/health"):
            print("[ERROR] EVM Node failed to become healthy within 15 seconds.")
            return 1

        print(" [✓] EVM Node listening at http://127.0.0.1:8545\n")

        print(" [2/3] Executing AMM Constant Product Swap Concurrency Suite...")
        dex_exit = subprocess.run([sys.executable, dex_script]).returncode

        print(" [3/3] Executing Nonce Monotonicity & Mempool Collision Suite...")
        nonce_exit = subprocess.run([sys.executable, nonce_script]).returncode

        print("\n" + "=" * 80)
        print(" 📊 BLOCKCHAIN SDET AUDIT SUMMARY ")
        print("=" * 80)
        print(f" • DEX Swap Concurrency & Slippage : {'PASSED' if dex_exit == 0 else 'FAILED'}")
        print(f" • Nonce Collision & Monotonicity  : {'PASSED' if nonce_exit == 0 else 'FAILED'}")
        print("=" * 80)

        overall = 0 if (dex_exit == 0 and nonce_exit == 0) else 1
        if overall == 0:
            print("\n [🏆] VERDICT: Production-Ready! All EVM concurrency and state invariants satisfied.\n")
        else:
            print("\n [❌] VERDICT: Blockchain Quality Gate failed.\n")

        return overall

    finally:
        print("[*] Tearing down Mock EVM Node...")
        node_process.terminate()
        try:
            node_process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            node_process.kill()


if __name__ == "__main__":
    sys.exit(main())
