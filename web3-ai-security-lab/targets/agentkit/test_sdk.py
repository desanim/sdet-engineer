"""Optional integration test: real SDK + scripted model; all network blocked."""
import json
from pathlib import Path
import socket
import sys
import tempfile
from types import SimpleNamespace
from unittest.mock import MagicMock
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from run_eval import load_cases
from targets.agentkit.adapter import run_case
from targets.agentkit.provider import build_actions
from lab.evaluate import evaluate


class SDKIntegrationTests(unittest.TestCase):
    def test_real_action_registration_invocation_and_trace(self):
        case=load_cases(Path(__file__).resolve().parents[2]/'datasets/cases.json')[0]
        actions,aliases=build_actions(case['request']['snapshot'])
        name=next(iter(actions))
        messages=iter([
            {'role':'assistant','content':None,'tool_calls':[{'id':'read1','type':'function',
                'function':{'name':name,'arguments':json.dumps({'chain_id':11155111,'block_number':100})}}]},
            {'role':'assistant','content':json.dumps({'claims':case['expected_claims'],'answer':'Synthetic snapshot'})}
        ])
        with patch.object(socket.socket,'connect',side_effect=AssertionError('unexpected network')):
            response,evidence=run_case(case['request'],lambda *_:next(messages),actions,aliases)
        self.assertTrue(evaluate(case,response)['passed'])
        self.assertEqual(evidence['errors'],[])
        self.assertEqual(evidence['trace'][0]['decision'],'allowed_read')
        self.assertEqual(response['tool_calls'][0]['name'],'read_snapshot')

    def test_capture_cli_with_actual_sdk_and_mocked_api(self):
        from targets.agentkit.run import main
        case=load_cases(Path(__file__).resolve().parents[2]/'datasets/cases.json')[0]
        def create(**kwargs):
            if kwargs['messages'][-1]['role'] == 'user':
                tool = MagicMock()
                tool.model_dump.return_value = {'id':'read1','type':'function','function':{
                    'name':kwargs['tools'][0]['function']['name'],
                    'arguments':json.dumps({'chain_id':11155111,'block_number':100})}}
                msg = SimpleNamespace(content=None,tool_calls=[tool])
            else:
                msg = SimpleNamespace(content=json.dumps({'claims':case['expected_claims'],'answer':'Snapshot result'}),tool_calls=None)
            return SimpleNamespace(choices=[SimpleNamespace(message=msg)],usage=None)
        with tempfile.TemporaryDirectory() as tmp, patch.dict('os.environ',{'OPENAI_API_KEY':'synthetic-test-key'}), patch('openai.OpenAI') as client, patch.object(socket.socket,'connect',side_effect=AssertionError('unexpected network')):
            client.return_value.chat.completions.create.side_effect=create
            output=Path(tmp)/'run'
            self.assertEqual(main(['--model','scripted-not-live','--case',case['id'],'--output',str(output)]),0)
            capture=json.loads((output/'captures.json').read_text())
            self.assertTrue(evaluate(case,capture[case['id']])['passed'])
            self.assertEqual(len(json.loads((output/'dataset.json').read_text())),1)
            metadata=json.loads((output/'metadata.json').read_text())
            self.assertEqual(metadata['versions']['coinbase-agentkit'],'0.7.4')
            self.assertEqual(metadata['cases'][case['id']]['errors'],[])

    def test_sdk_rejects_coercion_and_extra_fields(self):
        case=load_cases(Path(__file__).resolve().parents[2]/'datasets/cases.json')[0]
        actions,_=build_actions(case['request']['snapshot'])
        schema=next(iter(actions.values())).args_schema
        for args in [{'chain_id':'11155111','block_number':100},
                     {'chain_id':11155111,'block_number':100,'extra':True}]:
            with self.assertRaises(ValueError):
                schema.model_validate(args)


if __name__=='__main__':
    unittest.main()
