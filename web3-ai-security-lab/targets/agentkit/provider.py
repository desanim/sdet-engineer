"""Actual AgentKit action provider, without a wallet or transaction capability."""
import json
from unittest.mock import patch
from coinbase_agentkit import ActionProvider, create_action
from pydantic import BaseModel, ConfigDict, StrictInt


class SnapshotArgs(BaseModel):
    model_config = ConfigDict(extra='forbid')
    chain_id: StrictInt
    block_number: StrictInt


class SnapshotActionProvider(ActionProvider):
    def __init__(self, snapshot):
        self.snapshot = snapshot
        super().__init__('lab-snapshot', [])

    def supports_network(self, network):
        return True  # Synthetic data only; no network connection exists.

    @create_action(name='read_snapshot', description='Read the fixed synthetic blockchain snapshot.', schema=SnapshotArgs)
    def read_snapshot(self, args):
        parsed = SnapshotArgs.model_validate(args)
        if parsed.chain_id != self.snapshot['chain_id'] or parsed.block_number != self.snapshot['block_number']:
            raise ValueError('snapshot scope mismatch')
        return json.dumps(self.snapshot)


def build_actions(snapshot):
    # No wallet argument is used by the decorated action.
    actions = SnapshotActionProvider(snapshot).get_actions(None)
    if len(actions) != 1:
        raise RuntimeError('unexpected AgentKit action registry')
    action = actions[0]
    original = action.invoke

    def invoke_without_telemetry(args):
        # 0.7.4 has no telemetry opt-out; keep this sandbox's tools fully offline.
        with patch('coinbase_agentkit.action_providers.action_decorator.send_analytics_event'):
            return original(args)

    action.invoke = invoke_without_telemetry
    return {action.name: action}, {action.name: 'read_snapshot'}
