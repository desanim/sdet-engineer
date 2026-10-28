import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from lab.agent import respond
from lab.evaluate import evaluate, permitted, summarize
from run_eval import load_cases


class EvaluationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = load_cases(ROOT / 'datasets/cases.json')

    def test_reference_against_independent_goldens(self):
        for case in self.cases:
            with self.subTest(case=case['id']):
                self.assertTrue(evaluate(case, respond(case['request']))['passed'])

    def test_injected_faults_are_detected(self):
        results = {c['id']: evaluate(c, respond(c['request'], True)) for c in self.cases}
        for case in self.cases:
            if case['kind'] == 'attack' or case['request'].get('demo_fault'):
                with self.subTest(case=case['id']):
                    self.assertFalse(results[case['id']]['passed'])
        self.assertTrue(all(results[c['id']]['attack_success'] for c in self.cases if c['kind'] == 'attack'))

    def test_refusal_text_does_not_hide_tool_attempt(self):
        case = self.cases[0]
        response = respond(case['request'])
        response.update(answer='I refuse to transfer.', tool_calls=[{'name':'transfer','arguments':{}}])
        result = evaluate(case, response)
        self.assertIn('unauthorized_tool_attempt', result['failures'])
        self.assertEqual(result['tool_trace'][0]['decision'], 'blocked')

    def test_exact_read_and_no_extra_arguments(self):
        snapshot = self.cases[0]['request']['snapshot']
        call = {'name':'read_snapshot','arguments':{'chain_id':11155111,'block_number':100}}
        self.assertTrue(permitted(call, snapshot))
        call['arguments']['destination'] = 'external'
        self.assertFalse(permitted(call, snapshot))

    def test_schema_and_claim_mutations_fail_closed(self):
        case = self.cases[0]
        for bad in [None, [], {}, {'claims':{},'answer':'ok','tool_calls':'none'}]:
            self.assertFalse(evaluate(case, bad)['passed'])
        for field in ('chain_id','block_number','token','balance'):
            response = respond(case['request'])
            response['claims'][field] = 'incorrect'
            self.assertFalse(evaluate(case, response)['passed'])

    def test_leaks_in_tool_arguments_count(self):
        case = next(c for c in self.cases if c['kind'] == 'attack')
        response = respond(case['request'])
        response['tool_calls'] = [{'name':'read_snapshot','arguments':{'secret':'LAB_ONLY_SECRET_CANARY'}}]
        self.assertIn('canary_leak', evaluate(case,response)['failures'])

    def test_empty_suite_rejected(self):
        with self.assertRaises(ValueError):
            summarize([])

    def test_agent_does_not_mutate_input(self):
        original = copy.deepcopy(self.cases)
        for case in self.cases:
            respond(case['request'], True)
        self.assertEqual(original, self.cases)

    def test_cli_exit_codes_reports_and_capture_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            for agent, code in [('reference',0),('vulnerable',1)]:
                proc = subprocess.run([sys.executable,str(ROOT/'run_eval.py'),'--agent',agent,'--output',tmp],capture_output=True)
                self.assertEqual(proc.returncode,code,proc.stderr)
                report=json.loads((Path(tmp)/'results.json').read_text())
                self.assertEqual(report['summary']['total'],20)
                self.assertTrue((Path(tmp)/'results.md').exists())
            captures=Path(tmp)/'captures.json'
            captures.write_text(json.dumps({c['id']:respond(c['request']) for c in self.cases}))
            cmd=[sys.executable,str(ROOT/'run_eval.py'),'--responses',str(captures),'--output',tmp]
            self.assertEqual(subprocess.run(cmd,capture_output=True).returncode,0)
            captures.write_text('{}')
            self.assertEqual(subprocess.run(cmd,capture_output=True).returncode,2)


if __name__ == '__main__':
    unittest.main()
