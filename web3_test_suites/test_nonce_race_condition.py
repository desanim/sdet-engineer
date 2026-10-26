"""
EVM Nonce Synchronization & Mempool Conflict Test.
Simulates high-speed trading bots submitting concurrent transactions from a single wallet.
Verifies EVM nonce monotonicity rules and detects nonce collisions.
"""
import asyncio
import sys
import httpx

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

RPC_URL = "http://127.0.0.1:8545"


async def test_nonce_race_conditions():
    print("\n" + "=" * 80)
    print(" 🔢 WEB3 TEST SUITE: EVM NONCE MONOTONICITY & MEMPOOL RACE CONDITIONS ")
    print("=" * 80)

    sender_wallet = "0x742d35cc6634c0532925a3b844bc454e4438f44e"

    async with httpx.AsyncClient(base_url=RPC_URL, timeout=30.0) as client:
        # Step 1: Query current nonce
        nonce_payload = {
            "jsonrpc": "2.0",
            "method": "eth_getTransactionCount",
            "params": [sender_wallet, "latest"],
            "id": 1,
        }
        res = await client.post("/", json=nonce_payload)
        assert res.status_code == 200
        initial_nonce = int(res.json()["result"], 16)
        print(f"[*] Starting Baseline Nonce for {sender_wallet}: {initial_nonce}")

        # Step 2: Concurrent dispatch of 6 transactions with sequential nonces
        print("[*] Firing 6 concurrent transactions with sequential nonces...")

        async def send_tx(tx_index: int, nonce_val: int):
            payload = {
                "jsonrpc": "2.0",
                "method": "eth_sendTransaction",
                "params": [{
                    "from": sender_wallet,
                    "to": f"0x000000000000000000000000000000000000000{tx_index}",
                    "value": "0x2386f26fc10000",
                    "nonce": hex(nonce_val),
                }],
                "id": 10 + tx_index,
            }
            try:
                r = await client.post("/", json=payload)
                return {"index": tx_index, "nonce": nonce_val, "status": r.status_code, "resp": r.json()}
            except Exception as e:
                return {"index": tx_index, "nonce": nonce_val, "status": 500, "error": str(e)}

        tasks = [send_tx(i, initial_nonce + i) for i in range(6)]
        results = await asyncio.gather(*tasks)

        successful = [r for r in results if "result" in r.get("resp", {})]
        print(f" • Successfully ingested into Mempool: {len(successful)} / 6 transactions")
        for s in successful:
            print(f"   ↳ Tx Nonce {s['nonce']}: Hash {s['resp']['result'][:18]}...")

        # Step 3: Intentional Nonce Collision Attack (Replay / Stale Nonce)
        print("\n[*] Testing Stale Nonce Rejection (Sending tx with stale nonce 0)...")
        stale_payload = {
            "jsonrpc": "2.0",
            "method": "eth_sendTransaction",
            "params": [{
                "from": sender_wallet,
                "to": "0x0000000000000000000000000000000000000000",
                "value": "0x0",
                "nonce": "0x0",
            }],
            "id": 99,
        }
        stale_res = await client.post("/", json=stale_payload)
        resp_json = stale_res.json()

        assert "error" in resp_json, "Expected EVM node to reject stale nonce!"
        error_msg = resp_json["error"]["message"]
        print(f" [✓] PASS: EVM Node correctly rejected stale nonce: '{error_msg}'")

        print("=" * 80 + "\n")


if __name__ == "__main__":
    asyncio.run(test_nonce_race_conditions())
