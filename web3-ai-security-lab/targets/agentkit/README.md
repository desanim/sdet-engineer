# AgentKit target: real model, synthetic blockchain tools

This target runs a real tool-calling model through an actual Coinbase AgentKit custom action provider. It creates **no wallet**, uses **no CDP credentials**, and cannot sign or broadcast transactions. It evaluates our custom snapshot agent, not all of AgentKit or its default wallet chatbot.

The optional target has extra dependencies; the original offline lab remains standard-library only. Tested SDK environment: Python 3.12. Direct dependency versions are pinned in `requirements.txt`; transitive dependencies are not a full lockfile. Solana is pinned because AgentKit 0.7.4 imports `solana.rpc.api`.

## 1. Install (from repository root)

```bash
python -m venv .venv-agentkit
# Linux/macOS:
source .venv-agentkit/bin/activate
# Windows PowerShell instead:
# .\.venv-agentkit\Scripts\Activate.ps1
python -m pip install -r web3-ai-security-lab/targets/agentkit/requirements.txt
python web3-ai-security-lab/targets/agentkit/test_sdk.py -v
```

The SDK tests use scripted model responses and block network connections. They validate action registration, invocation, argument validation and canonical trace names; they do not measure LLM behavior.

## 2. Configure your model locally

Set `OPENAI_API_KEY` in your terminal environment or local secret manager. Do not paste it into chat or commit it. This runner reads environment variables, not `.env` files. The SDK uses OpenAI by default; choose a model in your account supporting Chat Completions function tools and `max_completion_tokens`.

No API key is needed for SDK/offline tests. Live requests incur your provider's API charges. Each case is bounded to 4 model requests, 1,500 completion tokens per request, a 45-second request timeout and no automatic retry. These limits are not a monetary budget.

## 3. Smoke-test one case

Replace `YOUR_MODEL_ID` with an available model ID:

```bash
python web3-ai-security-lab/targets/agentkit/run.py --model YOUR_MODEL_ID --case balance-six-decimals --output web3-ai-security-lab/reports/agentkit-smoke
python web3-ai-security-lab/run_eval.py --dataset web3-ai-security-lab/reports/agentkit-smoke/dataset.json --responses web3-ai-security-lab/reports/agentkit-smoke/captures.json --output web3-ai-security-lab/reports/agentkit-smoke/evaluation
```

## 4. Run all 20 scenarios

```bash
python web3-ai-security-lab/targets/agentkit/run.py --model YOUR_MODEL_ID --output web3-ai-security-lab/reports/agentkit-run-1
python web3-ai-security-lab/run_eval.py --dataset web3-ai-security-lab/reports/agentkit-run-1/dataset.json --responses web3-ai-security-lab/reports/agentkit-run-1/captures.json --output web3-ai-security-lab/reports/agentkit-run-1/evaluation
```

Use a new output directory for each run. Capture exit 0 means collection completed, not that the model passed evaluation. Capture errors return 2. The evaluator separately returns 0/1/2 for pass/fail/input error.

Outputs:

- `captures.json`: final structured claims, answer and dispatcher-observed tool calls.
- `dataset.json`: matching test subset for exact-ID evaluation.
- `metadata.json`: model name, prompt hash/version, dependency versions, timestamp, usage, latency, raw tool names, boundary decisions and errors.

Generated captures are ignored by git under `reports/`. They may contain malicious synthetic text; treat reports as data, never executable instructions.

## How the integration works

`provider.py` registers a real AgentKit `SnapshotActionProvider`. The adapter advertises its SDK-generated action name to the model. The model must request the snapshot, then produce `claims` and `answer`. Test goldens and `demo_fault` are never sent to the model.

The adapter records every requested call before checking authorization, maps only the registered action name to `read_snapshot`, validates arguments, and invokes the action only for the exact chain and block. Unknown names, writes and out-of-scope requests are blocked and remain in the capture even if the model later refuses. Model-supplied `tool_calls` inside final JSON are rejected; the dispatcher owns the trace.

AgentKit 0.7.4's decorator sends analytics without an opt-out. This sandbox suppresses that specific analytics callback during its action invocation using a scoped patch. This is tested with sockets blocked; it does not disable LLM network requests. Do not reuse this scoped patch in a concurrent production service.

## Limits and interpretation

Only the read action is advertised, so this first stage measures an agent with limited capabilities; it does not measure whether a model can safely choose among real fund-moving actions. The canary is synthetic and deliberately placed in the system context for the leak test. The evaluator scans final output and call arguments; intermediate assistant text and encoded leaks are not comprehensively graded.

The eight adversarial cases were designed for the mock suite and are an initial smoke benchmark, not a broad live-model red-team evaluation. SDK success does not imply a live-model pass. Repeated runs, held-out attacks, semantic review and richer transaction policies remain future work.

## Nên thử gì trước?

1. Chạy `test_sdk.py` để kiểm tra cài đặt, không tốn API.
2. Chạy một case balance với model của bạn, xem trace `allowed_read`.
3. Chạy cả bộ; xem lỗi claims, canary leak và tool call trái phép riêng biệt.
4. Lặp với thư mục mới để quan sát tính biến thiên của LLM; không sửa golden chỉ để test pass.

Sources: [AgentKit](https://github.com/coinbase/agentkit), [action provider API](https://github.com/coinbase/agentkit/blob/main/python/coinbase-agentkit/coinbase_agentkit/action_providers/action_provider.py). The implementation is tested against the pinned package, not an assumed latest API.
