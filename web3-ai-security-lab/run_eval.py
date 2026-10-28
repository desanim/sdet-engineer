#!/usr/bin/env python3
"""Run offline baselines or evaluate captured agent responses by case ID."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
from lab.agent import respond
from lab.evaluate import evaluate, summarize

ROOT = Path(__file__).resolve().parent


def load_cases(path):
    cases = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(cases, list) or not cases:
        raise ValueError('dataset must be a nonempty array')
    ids = [c['id'] for c in cases]
    if len(set(ids)) != len(ids):
        raise ValueError('duplicate case IDs')
    for c in cases:
        if c['kind'] not in ('benign', 'attack') or not isinstance(c['expected_claims'], dict):
            raise ValueError('invalid case contract')
        if 'expected_claims' in c['request']:
            raise ValueError('oracle must not be in agent input')
    return cases


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--agent', choices=['reference', 'vulnerable'], default='reference')
    p.add_argument('--responses', type=Path, help='JSON object mapping every case ID to captured response')
    p.add_argument('--dataset', type=Path, default=ROOT / 'datasets/cases.json')
    p.add_argument('--output', type=Path, default=ROOT / 'reports')
    args = p.parse_args(argv)
    try:
        cases = load_cases(args.dataset)
        captured = json.loads(args.responses.read_text(encoding='utf-8')) if args.responses else None
        if captured is not None and (not isinstance(captured, dict) or set(captured) != {c['id'] for c in cases}):
            raise ValueError('response IDs must exactly match dataset IDs')
        responses = captured if captured is not None else {
            c['id']: respond(c['request'], args.agent == 'vulnerable') for c in cases}
        results = [evaluate(c, responses[c['id']]) for c in cases]
        summary = summarize(results)
        report = {'mode': 'captured' if captured is not None else 'offline-' + args.agent,
                  'dataset_sha256': hashlib.sha256(args.dataset.read_bytes()).hexdigest(),
                  'limitations': 'Structured claims only; prose semantics not graded. No live LLM or transactions.',
                  'summary': summary, 'results': results}
        args.output.mkdir(parents=True, exist_ok=True)
        (args.output / 'results.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
        # Do not copy untrusted model text or tool arguments into Markdown reports.
        lines = ['# Web3 AI Security Evaluation', '', f"Mode: {report['mode']}", '',
                 report['limitations'], '', f"Passed: {summary['passed']}/{summary['total']}", '',
                 '| Case | Type | Result | Findings |', '|---|---|---|---|']
        for i, r in enumerate(results, 1):
            lines.append(f"| {i} | {r['kind']} | {'PASS' if r['passed'] else 'FAIL'} | {', '.join(r['failures']) or 'none'} |")
        (args.output / 'results.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
        print(json.dumps(summary, indent=2))
        return 0 if summary['gate_passed'] else 1
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'Evaluation input error: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
