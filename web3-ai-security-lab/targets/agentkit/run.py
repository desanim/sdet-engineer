"""Run a real model against AgentKit snapshot actions; never creates a wallet."""
import argparse
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from run_eval import load_cases
from targets.agentkit.adapter import PROMPT_VERSION, SYSTEM, run_case


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', required=True, help='Tool-calling model available in your OpenAI account')
    parser.add_argument('--dataset', type=Path, default=ROOT/'datasets/cases.json')
    parser.add_argument('--output', type=Path, default=ROOT/'reports/agentkit')
    parser.add_argument('--case', help='Run one case; writes a matching dataset subset for evaluation')
    args = parser.parse_args(argv)
    if not os.environ.get('OPENAI_API_KEY'):
        parser.error('Set OPENAI_API_KEY in your local environment; do not put it in the repository.')
    try:
        from openai import OpenAI
        from targets.agentkit.provider import build_actions
        cases = load_cases(args.dataset)
        if args.case:
            cases = [c for c in cases if c['id'] == args.case]
            if not cases:
                raise ValueError('unknown case ID')
        client = OpenAI(timeout=45, max_retries=0)
        if args.output.exists() and any(args.output.iterdir()):
            raise ValueError('output directory must be empty; select a new run directory')
        args.output.mkdir(parents=True, exist_ok=True)
        captures, evidence = {}, {}
        usage = []

        def complete(messages, tools):
            result = client.chat.completions.create(model=args.model, messages=messages,
                tools=tools, max_completion_tokens=1500)
            usage.append(result.usage.model_dump() if result.usage else {})
            msg = result.choices[0].message
            payload = {'role':'assistant','content':msg.content}
            if msg.tool_calls:
                payload['tool_calls'] = [t.model_dump() for t in msg.tool_calls]
            return payload

        start = time.monotonic()
        for case in cases:
            actions, aliases = build_actions(case['request']['snapshot'])
            before = time.monotonic()
            response, detail = run_case(case['request'], complete, actions, aliases)
            captures[case['id']] = response
            evidence[case['id']] = {**detail,'elapsed_seconds':time.monotonic()-before}
            print(f"Captured {case['id']}")
        metadata = {'mode':'live-model-synthetic-tools','model':args.model,
            'prompt_version':PROMPT_VERSION,'prompt_sha256':hashlib.sha256(SYSTEM.encode()).hexdigest(),
            'source_dataset_sha256':hashlib.sha256(args.dataset.read_bytes()).hexdigest(),
            'timestamp_utc':datetime.now(timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-start,
            'versions':{p:version(p) for p in ('openai','coinbase-agentkit')},
            'usage':usage,'cases':evidence}
        for filename, data in [('captures.json',captures),('dataset.json',cases),('metadata.json',metadata)]:
            (args.output/filename).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
        print('Capture complete. Run run_eval.py with the saved dataset and captures to obtain a verdict.')
        return 0
    except Exception as exc:
        # Avoid printing provider exception bodies that may contain request data.
        print(f'Capture failed ({type(exc).__name__}); no completed run was produced.',file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
