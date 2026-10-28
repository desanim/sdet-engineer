"""Offline tests for the live adapter; no model API credentials needed."""
import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from run_eval import load_cases
from targets.agentkit.adapter import agent_input, run_case
from lab.evaluate import evaluate


class FakeSchema:
    @staticmethod
    def model_json_schema():
        return {'type':'object','properties':{}}

    @staticmethod
    def model_validate(args):
        return args


class FakeAction:
    description = 'Read synthetic snapshot'
    args_schema = FakeSchema

    def __init__(self, snapshot):
        self.snapshot = snapshot
        self.invocations = []

    def invoke(self, args):
        self.invocations.append(args)
        return json.dumps(self.snapshot)


def call(name, args):
    return {'role':'assistant','content':None,'tool_calls':[{
        'id':'call_1','type':'function','function':{'name':name,'arguments':json.dumps(args)}}]}


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.case = load_cases(Path(__file__).resolve().parents[1]/'datasets/cases.json')[0]
        self.action = FakeAction(self.case['request']['snapshot'])
        self.actions = {'SnapshotActionProvider_read_snapshot':self.action}
        self.aliases = {'SnapshotActionProvider_read_snapshot':'read_snapshot'}

    def run_messages(self, messages, turns=4):
        scripted = iter(messages)
        return run_case(self.case['request'],lambda *_:next(scripted),self.actions,self.aliases,turns)

    def final(self):
        return {'role':'assistant','content':json.dumps({'claims':self.case['expected_claims'],'answer':'Snapshot result'})}

    def test_goldens_and_fault_labels_never_enter_request(self):
        request = copy.deepcopy(self.case['request'])
        request['expected_claims'] = {'secret':'oracle'}
        result = agent_input(request)
        self.assertNotIn('demo_fault',result)
        self.assertNotIn('expected_claims',result)
        self.assertNotIn('raw_balance',json.dumps(result))

    def test_real_observed_read_is_canonicalized(self):
        response,evidence = self.run_messages([call(next(iter(self.actions)),{'chain_id':11155111,'block_number':100}),self.final()])
        self.assertTrue(evaluate(self.case,response)['passed'])
        self.assertEqual(len(self.action.invocations),1)
        self.assertEqual(evidence['trace'][0]['decision'],'allowed_read')

    def test_forbidden_call_cannot_be_erased_by_final_answer(self):
        response,evidence = self.run_messages([call('transfer',{'amount':'100'}),self.final()])
        self.assertIn('unauthorized_tool_attempt',evaluate(self.case,response)['failures'])
        self.assertEqual(evidence['trace'][0]['decision'],'blocked')
        self.assertEqual(self.action.invocations,[])

    def test_wrong_chain_and_extra_parameters_blocked(self):
        for args in [{'chain_id':1,'block_number':100},{'chain_id':11155111,'block_number':100,'to':'x'}]:
            response,_ = self.run_messages([call(next(iter(self.actions)),args),self.final()])
            self.assertFalse(evaluate(self.case,response)['passed'])
        self.assertEqual(self.action.invocations,[])

    def test_invalid_arguments_and_final_json_fail(self):
        bad=call('transfer',{})
        bad['tool_calls'][0]['function']['arguments']='{bad json'
        response,evidence=self.run_messages([bad,{'role':'assistant','content':'not json'}])
        self.assertFalse(evaluate(self.case,response)['passed'])
        self.assertIn('invalid_model_output',evidence['errors'])
        self.assertEqual(len(response['tool_calls']),1)

    def test_model_cannot_supply_its_own_trace(self):
        final=self.final()
        data=json.loads(final['content']); data['tool_calls']=[]
        final['content']=json.dumps(data)
        response,evidence=self.run_messages([call('approve',{}),final])
        self.assertEqual(response['tool_calls'][0]['name'],'unregistered:approve')
        self.assertIn('invalid_model_output',evidence['errors'])

    def test_unregistered_alias_cannot_look_like_authorized_read(self):
        response,evidence=self.run_messages([call('read_snapshot',{'chain_id':11155111,'block_number':100}),self.final()])
        self.assertIn('unauthorized_tool_attempt',evaluate(self.case,response)['failures'])
        self.assertEqual(evidence['trace'][0]['decision'],'blocked')
        self.assertEqual(self.action.invocations,[])

    def test_turn_limit_fails_with_trace(self):
        response,evidence=self.run_messages([call('sign_transaction',{})],turns=1)
        self.assertFalse(evaluate(self.case,response)['passed'])
        self.assertIn('turn_limit',evidence['errors'])
