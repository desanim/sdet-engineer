"""
Automated Accessibility (A11y) & UX Quality Gate Runner.
Audits Web3 / DApp frontend interfaces against WCAG 2.1 Level AA conformance criteria.
"""
import argparse
import json
import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from a11y_engine.wcag_validator import WCAGValidator


def run_audit(html_path: str, output_dir: str) -> int:
    if not os.path.exists(html_path):
        print(f"[ERROR] Target HTML file not found: {html_path}")
        return 1

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    print("\n" + "=" * 85)
    print(" ♿ SDET ACCESSIBILITY & UX AUDITOR: WCAG 2.1 LEVEL AA CONFORMANCE SCAN ")
    print("=" * 85)
    print(f" • Target Interface: {html_path}")
    print(f" • Target Standard : WCAG 2.1 (Level A & Level AA)")
    print(f" • Methodologies   : Automated Static Analysis + Rule Invariants")
    print("=" * 85 + "\n")

    validator = WCAGValidator(html_content)
    results = validator.run_all_checks()

    # Console Summary Table
    print(f"{'CRITERION':<35} | {'SEVERITY':<10} | {'STATUS':<8} | {'DETAIL':<25}")
    print("-" * 85)

    for p in results["passes"]:
        crit = p["criterion"][:33]
        print(f"{crit:<35} | {'None':<10} | {'PASS':<8} | {p['detail'][:25]}...")

    for v in results["violations"]:
        crit = v["criterion"][:33]
        sev = v["severity"]
        print(f"{crit:<35} | {sev:<10} | {'FAIL':<8} | {v['message'][:25]}...")

    print("-" * 85)
    score = results["compliance_score_percent"]
    passed = results["passed_count"]
    violations = results["violation_count"]
    print(f"SUMMARY: Compliance Score: {score}% | Passed: {passed} | Violations: {violations}")
    print("=" * 85 + "\n")

    # Detailed Violation Breakdown
    if results["violations"]:
        print("[⚠️] DETECTED ACCESSIBILITY VIOLATIONS & REMEDIATION GUIDANCE:\n")
        for i, v in enumerate(results["violations"], 1):
            print(f" {i}. [{v['severity'].upper()}] {v['criterion']}")
            print(f"    • Offending Element: {v['element']}")
            print(f"    • Problem          : {v['message']}")
            if "remediation" in v:
                print(f"    • How to Fix       : {v['remediation']}")
            print()

    # Export Artifacts
    os.makedirs(output_dir, exist_ok=True)
    json_path = os.path.join(output_dir, "a11y_audit_report.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    md_path = os.path.join(output_dir, "a11y_audit_report.md")
    generate_markdown_report(results, md_path)

    print(f"[+] Saved JSON Audit Report to: {json_path}")
    print(f"[+] Saved Markdown Report to   : {md_path}\n")

    critical_count = sum(1 for v in results["violations"] if v["severity"] == "Critical")
    if critical_count > 0:
        print(f"[❌] QUALITY GATE FAILED: Found {critical_count} Critical A11y violations blocking release.\n")
        return 1
    else:
        print("[✓] QUALITY GATE PASSED: Conforms to baseline accessibility requirements.\n")
        return 0


def generate_markdown_report(results: dict, output_file: str):
    score = results["compliance_score_percent"]
    status_badge = "❌ **FAILED (CRITICAL A11Y DEFECTS FOUND)**" if results["violation_count"] > 0 else "✅ **PASSED (WCAG 2.1 AA COMPLIANT)**"

    lines = [
        "# ♿ Web3 DApp UX & Accessibility (A11y) Quality Audit Report\n",
        f"**Audit Result**: {status_badge}  ",
        f"**Compliance Score**: `{score}%` | **Total Rules Scanned**: `{results['total_checks']}` | **Violations**: `{results['violation_count']}`\n",
        "## 1. Conformance Matrix\n",
        "| Success Criterion | WCAG Level | Status | Details |",
        "| :--- | :--- | :--- | :--- |",
    ]

    for p in results["passes"]:
        lines.append(f"| `{p['criterion']}` | A / AA | ✅ **PASS** | {p['detail']} |")

    for v in results["violations"]:
        lines.append(f"| `{v['criterion']}` | A / AA | ❌ **FAIL** ({v['severity']}) | {v['message']} |")

    if results["violations"]:
        lines.append("\n## 2. Remediation Action Plan (Defect Backlog)\n")
        for i, v in enumerate(results["violations"], 1):
            lines.append(f"### Defect {i}: {v['criterion']} [{v['severity']}]")
            lines.append(f"- **Affected Component**: `{v['element']}`")
            lines.append(f"- **Impact on User**: {v['message']}")
            if "remediation" in v:
                lines.append(f"- **Recommended Fix**: `{v['remediation']}`\n")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(description="Web3 UX Accessibility Scanner")
    parser.add_argument(
        "--html",
        default=os.path.join(os.path.dirname(__file__), "mock_dapp_ui", "index.html"),
        help="Path to target HTML file",
    )
    parser.add_argument(
        "--output-dir",
        default=os.path.join(os.path.dirname(__file__), "reports"),
        help="Output report directory",
    )
    args = parser.parse_args()
    code = run_audit(args.html, args.output_dir)
    sys.exit(code)


if __name__ == "__main__":
    main()
