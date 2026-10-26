"""
Web3 & Blockchain Performance Analyzer & Quality Gate.
Evaluates EVM RPC metrics: Sustained TPS, p95/p99 RPC latency, and mempool error rates.
"""
import argparse
import csv
import json
import math
import os
import sys
from collections import defaultdict
from typing import Dict, List, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def calculate_percentile(values: List[float], pct: float) -> float:
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    k = (len(sorted_vals) - 1) * (pct / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return float(sorted_vals[int(k)])
    return float(sorted_vals[int(f)] * (c - k) + sorted_vals[int(c)] * (k - f))


def parse_jtl(file_path: str) -> Tuple[Dict[str, List[dict]], float]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"JTL file not found: {file_path}")

    transactions = defaultdict(list)
    min_ts = float("inf")
    max_ts = 0.0

    with open(file_path, mode="r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                elapsed = float(row.get("elapsed", 0))
                label = row.get("label", "Unknown")
                success = str(row.get("success", "true")).strip().lower() in ("true", "1")
                ts = float(row.get("timeStamp", 0))

                if ts > 0:
                    min_ts = min(min_ts, ts)
                    max_ts = max(max_ts, ts + elapsed)

                transactions[label].append({
                    "elapsed": elapsed,
                    "success": success,
                    "code": row.get("responseCode", ""),
                })
            except (ValueError, KeyError):
                continue

    duration_sec = max((max_ts - min_ts) / 1000.0, 1.0)
    return transactions, duration_sec


def compute_metrics(transactions: Dict[str, List[dict]], duration_sec: float) -> dict:
    report = {"rpc_methods": {}, "summary": {}}
    all_elapsed = []
    total_samples = 0
    total_success = 0

    for label, samples in transactions.items():
        count = len(samples)
        elapsed_list = [s["elapsed"] for s in samples]
        succ = sum(1 for s in samples if s["success"])
        err = count - succ
        err_pct = (err / count * 100.0) if count > 0 else 0.0

        all_elapsed.extend(elapsed_list)
        total_samples += count
        total_success += succ

        report["rpc_methods"][label] = {
            "samples": count,
            "errors": err,
            "error_rate_pct": round(err_pct, 2),
            "throughput_tps": round(count / duration_sec, 2),
            "min_ms": round(min(elapsed_list), 1) if elapsed_list else 0,
            "avg_ms": round(sum(elapsed_list) / count, 1) if elapsed_list else 0,
            "max_ms": round(max(elapsed_list), 1) if elapsed_list else 0,
            "p50_ms": round(calculate_percentile(elapsed_list, 50), 1),
            "p90_ms": round(calculate_percentile(elapsed_list, 90), 1),
            "p95_ms": round(calculate_percentile(elapsed_list, 95), 1),
            "p99_ms": round(calculate_percentile(elapsed_list, 99), 1),
        }

    total_err = total_samples - total_success
    overall_err_pct = (total_err / total_samples * 100.0) if total_samples > 0 else 0.0

    report["summary"] = {
        "duration_sec": round(duration_sec, 2),
        "total_requests": total_samples,
        "total_errors": total_err,
        "error_rate_pct": round(overall_err_pct, 2),
        "sustained_tps": round(total_samples / duration_sec, 2),
        "min_ms": round(min(all_elapsed), 1) if all_elapsed else 0,
        "avg_ms": round(sum(all_elapsed) / total_samples, 1) if all_elapsed else 0,
        "max_ms": round(max(all_elapsed), 1) if all_elapsed else 0,
        "p50_ms": round(calculate_percentile(all_elapsed, 50), 1),
        "p90_ms": round(calculate_percentile(all_elapsed, 90), 1),
        "p95_ms": round(calculate_percentile(all_elapsed, 95), 1),
        "p99_ms": round(calculate_percentile(all_elapsed, 99), 1),
    }

    return report


def evaluate_sla(metrics: dict, sla_config_path: str) -> Tuple[bool, List[str]]:
    violations = []
    if not os.path.exists(sla_config_path):
        return True, ["No SLA configuration found. Skipping quality gate."]

    with open(sla_config_path, "r", encoding="utf-8") as f:
        sla = json.load(f)

    global_sla = sla.get("global_blockchain_sla", {})
    summary = metrics["summary"]

    min_tps = global_sla.get("min_sustained_tps")
    if min_tps and summary["sustained_tps"] < min_tps:
        violations.append(
            f"[TPS BREACH] Sustained TPS: {summary['sustained_tps']} is below required minimum ({min_tps} TPS)"
        )

    max_p95 = global_sla.get("max_p95_rpc_latency_ms")
    if max_p95 and summary["p95_ms"] > max_p95:
        violations.append(
            f"[LATENCY BREACH] Overall p95: {summary['p95_ms']}ms exceeds SLA threshold ({max_p95}ms)"
        )

    max_err = global_sla.get("max_error_rate_percent")
    if max_err and summary["error_rate_pct"] > max_err:
        violations.append(
            f"[REVERT/ERROR BREACH] Error Rate: {summary['error_rate_pct']}% exceeds limit ({max_err}%)"
        )

    method_slas = sla.get("rpc_method_sla", {})
    for method_name, method_metrics in metrics["rpc_methods"].items():
        if method_name in method_slas:
            rule = method_slas[method_name]
            rule_p95 = rule.get("max_p95_ms")
            if rule_p95 and method_metrics["p95_ms"] > rule_p95:
                violations.append(
                    f"[{method_name} BREACH] p95: {method_metrics['p95_ms']}ms exceeds {rule_p95}ms"
                )

    passed = len(violations) == 0
    return passed, violations


def print_cli_summary(metrics: dict, passed: bool, violations: List[str]):
    print("\n" + "=" * 90)
    print(f"{'RPC METHOD':<28} | {'SAMPLES':<8} | {'ERR %':<6} | {'p50':<7} | {'p90':<7} | {'p95':<7} | {'TPS':<7}")
    print("-" * 90)

    for name, d in metrics["rpc_methods"].items():
        print(f"{name:<28} | {d['samples']:<8} | {d['error_rate_pct']:<5}% | {d['p50_ms']:<7} | {d['p90_ms']:<7} | {d['p95_ms']:<7} | {d['throughput_tps']:<7}")

    print("-" * 90)
    s = metrics["summary"]
    print(f"{'TOTAL / AGGREGATE':<28} | {s['total_requests']:<8} | {s['error_rate_pct']:<5}% | {s['p50_ms']:<7} | {s['p90_ms']:<7} | {s['p95_ms']:<7} | {s['sustained_tps']:<7}")
    print("=" * 90)

    if passed:
        print("\n [✓] BLOCKCHAIN QUALITY GATE: PASSED (All Web3 RPC SLAs Satisfied)\n")
    else:
        print("\n [❌] BLOCKCHAIN QUALITY GATE: FAILED (Thresholds Breached!)")
        for v in violations:
            print(f"   • {v}")
        print()


def generate_markdown_report(metrics: dict, violations: List[str], output_path: str):
    passed = len(violations) == 0
    badge = "✅ **PASSED (ALL BLOCKCHAIN SLAs SATISFIED)**" if passed else "❌ **FAILED (BLOCKCHAIN SLA BREACHED)**"

    lines = [
        "# ⛓️ Web3 & Blockchain Performance Quality Gate Report\n",
        f"**Quality Gate Status**: {badge}\n",
        f"**Benchmark Duration**: `{metrics['summary']['duration_sec']}s` | **Total Calls**: `{metrics['summary']['total_requests']}` | **Sustained TPS**: `{metrics['summary']['sustained_tps']}`\n",
        "\n### EVM JSON-RPC Methods Breakdown\n",
        "| RPC Method | Samples | Errors | Error % | p50 (ms) | p90 (ms) | p95 (ms) | p99 (ms) | Method TPS |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
    ]

    for name, d in metrics["rpc_methods"].items():
        lines.append(
            f"| `{name}` | {d['samples']} | {d['errors']} | {d['error_rate_pct']}% | {d['p50_ms']} | {d['p90_ms']} | **{d['p95_ms']}** | {d['p99_ms']} | **{d['throughput_tps']}** |"
        )

    s = metrics["summary"]
    lines.append(
        f"| **AGGREGATE** | **{s['total_requests']}** | **{s['total_errors']}** | **{s['error_rate_pct']}%** | **{s['p50_ms']}** | **{s['p90_ms']}** | **{s['p95_ms']}** | **{s['p99_ms']}** | **{s['sustained_tps']}** |\n"
    )

    if violations:
        lines.append("### ⚠️ SLA Violations\n")
        for v in violations:
            lines.append(f"- 🔴 {v}")
    else:
        lines.append("### ✨ Finality & Throughput Readiness\n- EVM Node meets enterprise throughput and latency criteria.\n")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(description="Web3 / Blockchain Performance Quality Gate Analyzer")
    parser.add_argument("--jtl", required=True, help="Path to JMeter .jtl log file")
    parser.add_argument("--sla-config", required=True, help="Path to web3_sla_config.json")
    parser.add_argument("--output-dir", default=".", help="Directory to export reports")

    args = parser.parse_args()
    transactions, duration = parse_jtl(args.jtl)
    metrics = compute_metrics(transactions, duration)
    passed, violations = evaluate_sla(metrics, args.sla_config)

    print_cli_summary(metrics, passed, violations)

    os.makedirs(args.output_dir, exist_ok=True)
    with open(os.path.join(args.output_dir, "web3_metrics.json"), "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    md_path = os.path.join(args.output_dir, "web3_summary.md")
    generate_markdown_report(metrics, violations, md_path)
    print(f"[+] Exported Markdown report to: {md_path}")

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
