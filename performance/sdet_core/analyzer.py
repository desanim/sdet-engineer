"""
SDET Performance Metrics Analyzer & Quality Gate Evaluator.
Parses JMeter .jtl logs, calculates percentiles & throughput, and validates against SLAs.
"""
import argparse
import csv
import json
import math
import os
import sys
from collections import defaultdict
from typing import Dict, List, Tuple


def calculate_percentile(values: List[float], percentile: float) -> float:
    """Calculates percentile using standard nearest-rank / linear interpolation."""
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    k = (len(sorted_vals) - 1) * (percentile / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return float(sorted_vals[int(k)])
    d0 = sorted_vals[int(f)] * (c - k)
    d1 = sorted_vals[int(c)] * (k - f)
    return float(d0 + d1)


def parse_jtl(file_path: str) -> Tuple[Dict[str, List[dict]], float, float]:
    """Parses a JMeter JTL/CSV result file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"JTL file not found: {file_path}")

    transactions = defaultdict(list)
    min_timestamp = float("inf")
    max_timestamp = 0.0

    with open(file_path, mode="r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                elapsed = float(row.get("elapsed", 0))
                label = row.get("label", "Unknown")
                success_val = str(row.get("success", "true")).strip().lower()
                success = success_val in ("true", "1")
                ts = float(row.get("timeStamp", 0))

                if ts > 0:
                    min_timestamp = min(min_timestamp, ts)
                    max_timestamp = max(max_timestamp, ts + elapsed)

                transactions[label].append({
                    "elapsed": elapsed,
                    "success": success,
                    "code": row.get("responseCode", ""),
                })
            except (ValueError, KeyError):
                continue

    duration_seconds = max((max_timestamp - min_timestamp) / 1000.0, 1.0)
    return transactions, duration_seconds


def compute_metrics(transactions: Dict[str, List[dict]], duration_seconds: float) -> dict:
    """Computes performance statistics for each transaction and overall."""
    report = {"transactions": {}, "summary": {}}
    all_elapsed = []
    all_success_count = 0
    total_samples = 0

    for label, samples in transactions.items():
        count = len(samples)
        elapsed_times = [s["elapsed"] for s in samples]
        successes = sum(1 for s in samples if s["success"])
        errors = count - successes
        error_rate = (errors / count * 100.0) if count > 0 else 0.0

        all_elapsed.extend(elapsed_times)
        all_success_count += successes
        total_samples += count

        report["transactions"][label] = {
            "samples": count,
            "errors": errors,
            "error_rate_pct": round(error_rate, 2),
            "throughput_rps": round(count / duration_seconds, 2),
            "min_ms": round(min(elapsed_times), 1) if elapsed_times else 0,
            "avg_ms": round(sum(elapsed_times) / count, 1) if elapsed_times else 0,
            "max_ms": round(max(elapsed_times), 1) if elapsed_times else 0,
            "p50_ms": round(calculate_percentile(elapsed_times, 50), 1),
            "p90_ms": round(calculate_percentile(elapsed_times, 90), 1),
            "p95_ms": round(calculate_percentile(elapsed_times, 95), 1),
            "p99_ms": round(calculate_percentile(elapsed_times, 99), 1),
        }

    total_errors = total_samples - all_success_count
    overall_error_rate = (total_errors / total_samples * 100.0) if total_samples > 0 else 0.0

    report["summary"] = {
        "duration_sec": round(duration_seconds, 2),
        "total_samples": total_samples,
        "total_errors": total_errors,
        "error_rate_pct": round(overall_error_rate, 2),
        "throughput_rps": round(total_samples / duration_seconds, 2),
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
    """Evaluates computed metrics against SLA quality gates."""
    violations = []
    if not os.path.exists(sla_config_path):
        return True, ["No SLA configuration found. Skipping quality gate check."]

    with open(sla_config_path, "r", encoding="utf-8") as f:
        sla = json.load(f)

    # 1. Global SLA Check
    global_sla = sla.get("global_sla", {})
    summary = metrics["summary"]

    max_err = global_sla.get("max_error_rate_percent")
    if max_err is not None and summary["error_rate_pct"] > max_err:
        violations.append(
            f"[GLOBAL SLA BREACH] Error Rate: {summary['error_rate_pct']}% exceeds threshold ({max_err}%)"
        )

    max_p95 = global_sla.get("max_p95_response_time_ms")
    if max_p95 is not None and summary["p95_ms"] > max_p95:
        violations.append(
            f"[GLOBAL SLA BREACH] Overall 95th Percentile: {summary['p95_ms']}ms exceeds threshold ({max_p95}ms)"
        )

    # 2. Transaction-specific SLA Check
    txn_slas = sla.get("transaction_sla", {})
    for txn_name, txn_metrics in metrics["transactions"].items():
        if txn_name in txn_slas:
            rule = txn_slas[txn_name]
            rule_p95 = rule.get("max_p95_ms")
            if rule_p95 is not None and txn_metrics["p95_ms"] > rule_p95:
                violations.append(
                    f"[{txn_name} SLA BREACH] p95: {txn_metrics['p95_ms']}ms exceeds threshold ({rule_p95}ms)"
                )

            rule_err = rule.get("max_error_rate_percent")
            if rule_err is not None and txn_metrics["error_rate_pct"] > rule_err:
                violations.append(
                    f"[{txn_name} SLA BREACH] Error Rate: {txn_metrics['error_rate_pct']}% exceeds threshold ({rule_err}%)"
                )

    passed = len(violations) == 0
    return passed, violations


def generate_markdown_report(metrics: dict, violations: List[str], output_path: str):
    """Outputs a GitHub Flavored Markdown report for CI/CD Step Summaries."""
    passed = len(violations) == 0
    status_badge = "✅ **PASSED (ALL SLAs SATISFIED)**" if passed else "❌ **FAILED (SLA BREACHED)**"

    md = []
    md.append(f"# SDET Performance Quality Gate Report\n")
    md.append(f"**Status**: {status_badge}\n")
    md.append(f"**Test Duration**: `{metrics['summary']['duration_sec']}s` | **Total Requests**: `{metrics['summary']['total_samples']}` | **Overall RPS**: `{metrics['summary']['throughput_rps']}`\n")

    md.append("\n### Transaction Metrics Breakdown\n")
    md.append("| Transaction | Samples | Errors | Error % | Avg (ms) | p90 (ms) | p95 (ms) | p99 (ms) | Throughput (RPS) |")
    md.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")

    for name, data in metrics["transactions"].items():
        md.append(
            f"| `{name}` | {data['samples']} | {data['errors']} | {data['error_rate_pct']}% | {data['avg_ms']} | {data['p90_ms']} | **{data['p95_ms']}** | {data['p99_ms']} | {data['throughput_rps']} |"
        )

    summ = metrics["summary"]
    md.append(
        f"| **TOTAL** | **{summ['total_samples']}** | **{summ['total_errors']}** | **{summ['error_rate_pct']}%** | **{summ['avg_ms']}** | **{summ['p90_ms']}** | **{summ['p95_ms']}** | **{summ['p99_ms']}** | **{summ['throughput_rps']}** |\n"
    )

    if violations:
        md.append("### ⚠️ SLA Violations Detected\n")
        for v in violations:
            md.append(f"- 🔴 {v}")
    else:
        md.append("### ✨ Quality Gate Status\n- All transactions and global metrics meet production readiness thresholds.\n")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))


def print_cli_summary(metrics: dict, passed: bool, violations: List[str]):
    """Prints a beautiful formatted ASCII table in console."""
    print("\n" + "=" * 90)
    print(f"{'TRANSACTION':<22} | {'SAMPLES':<8} | {'ERR %':<6} | {'AVG':<7} | {'p90':<7} | {'p95':<7} | {'p99':<7} | {'RPS':<6}")
    print("-" * 90)

    for name, d in metrics["transactions"].items():
        print(f"{name:<22} | {d['samples']:<8} | {d['error_rate_pct']:<5}% | {d['avg_ms']:<7} | {d['p90_ms']:<7} | {d['p95_ms']:<7} | {d['p99_ms']:<7} | {d['throughput_rps']:<6}")

    print("-" * 90)
    s = metrics["summary"]
    print(f"{'TOTAL / SUMMARY':<22} | {s['total_samples']:<8} | {s['error_rate_pct']:<5}% | {s['avg_ms']:<7} | {s['p90_ms']:<7} | {s['p95_ms']:<7} | {s['p99_ms']:<7} | {s['throughput_rps']:<6}")
    print("=" * 90)

    if passed:
        print("\n [✓] QUALITY GATE RESULT: PASSED (All performance SLAs are satisfied)\n")
    else:
        print("\n [❌] QUALITY GATE RESULT: FAILED (SLA Thresholds Breached!)")
        for v in violations:
            print(f"   • {v}")
        print()


def main():
    parser = argparse.ArgumentParser(description="SDET Performance Analyzer & Quality Gate Evaluator")
    parser.add_argument("--jtl", required=True, help="Path to JMeter .jtl log file")
    parser.add_argument("--sla-config", required=True, help="Path to sla_config.json")
    parser.add_argument("--output-dir", default=".", help="Directory to export reports")

    args = parser.parse_args()
    transactions, duration = parse_jtl(args.jtl)
    metrics = compute_metrics(transactions, duration)
    passed, violations = evaluate_sla(metrics, args.sla_config)

    print_cli_summary(metrics, passed, violations)

    # Export artifacts
    os.makedirs(args.output_dir, exist_ok=True)
    json_path = os.path.join(args.output_dir, "metrics_summary.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    md_path = os.path.join(args.output_dir, "summary.md")
    generate_markdown_report(metrics, violations, md_path)
    print(f"[+] Exported Markdown summary to: {md_path}")
    print(f"[+] Exported JSON metrics to:    {json_path}")

    # Exit code determines CI/CD pass/fail status
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
