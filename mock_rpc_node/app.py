"""
High-Performance EVM JSON-RPC Mock Node for Blockchain SDET Testing.
Simulates realistic Ethereum JSON-RPC 2.0 specifications:
- Block mining lifecycle & block numbers
- State storage for balances, nonces, and ERC-20 token reserves
- Mempool queueing & transaction receipt generation
- Concurrency race condition handling for Nonce & AMM Constant Product Swaps
"""
import asyncio
import hashlib
import json
import random
import sys
import time
import uuid
from typing import Any, Dict, List, Optional, Union

from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

app = FastAPI(
    title="EVM Mock JSON-RPC Node",
    description="Simulated Ethereum Node for Blockchain / Web3 SDET Load & Concurrency Testing",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# In-Memory Blockchain State
# ---------------------------------------------------------------------------
CHAIN_ID = 1  # Ethereum Mainnet
CURRENT_BLOCK = 19_000_000
BLOCK_GENESIS_TIME = time.time()

# Balances in Wei (1 ETH = 10^18 Wei)
BALANCES: Dict[str, int] = {}
NONCES: Dict[str, int] = {}

# Mempool: tx_hash -> tx_data
MEMPOOL: Dict[str, dict] = {}
RECEIPTS: Dict[str, dict] = {}

# AMM DEX Liquidity Pool: x * y = k (e.g. WETH / USDC)
# Reserve A (WETH): 1,000 ETH (in Wei)
# Reserve B (USDC): 3,000,000 USDC (6 decimals: 3_000_000 * 10^6)
AMM_RESERVE_WETH = 1000 * 10**18
AMM_RESERVE_USDC = 3_000_000 * 10**6
AMM_K = AMM_RESERVE_WETH * AMM_RESERVE_USDC
amm_mutex = asyncio.Lock()
nonce_mutex = asyncio.Lock()


def to_hex(val: int) -> str:
    """Formats an integer into standard Ethereum 0x hex string."""
    return hex(val)


def normalize_address(addr: str) -> str:
    return addr.lower() if addr else ""


# Seed predefined genesis accounts
for i in range(1, 201):
    acc = f"0x{i:040x}"
    BALANCES[acc] = 100 * 10**18  # 100 ETH
    NONCES[acc] = 0


# Background Block Mining Simulation (Mines a block every 1.5 seconds)
async def block_miner_worker():
    global CURRENT_BLOCK
    while True:
        await asyncio.sleep(1.5)
        CURRENT_BLOCK += 1
        
        # Mine pending transactions from mempool
        if MEMPOOL:
            mined_hashes = list(MEMPOOL.keys())[:50]  # Max 50 txs per block
            for th in mined_hashes:
                tx = MEMPOOL.pop(th, None)
                if not tx:
                    continue
                
                RECEIPTS[th] = {
                    "transactionHash": th,
                    "transactionIndex": "0x0",
                    "blockNumber": to_hex(CURRENT_BLOCK),
                    "blockHash": f"0x{hashlib.sha256(str(CURRENT_BLOCK).encode()).hexdigest()}",
                    "from": tx["from"],
                    "to": tx["to"],
                    "cumulativeGasUsed": "0x5208",
                    "gasUsed": "0x5208",  # 21,000 gas
                    "contractAddress": None,
                    "logs": [],
                    "status": "0x1",  # 0x1 = Success, 0x0 = Revert
                }


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(block_miner_worker())


# ---------------------------------------------------------------------------
# JSON-RPC Handler Implementation
# ---------------------------------------------------------------------------

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "chain_id": CHAIN_ID,
        "block_number": CURRENT_BLOCK,
        "mempool_size": len(MEMPOOL),
        "total_receipts": len(RECEIPTS),
    }


@app.post("/")
async def json_rpc_endpoint(request: Request):
    """Ethereum JSON-RPC 2.0 gateway supporting batch and single calls."""
    try:
        body = await request.json()
    except Exception:
        return {
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32700, "message": "Parse error"},
        }

    # Support JSON-RPC Batch requests
    if isinstance(body, list):
        results = [await process_single_rpc(req) for req in body]
        return results
    else:
        return await process_single_rpc(body)


async def process_single_rpc(payload: dict) -> dict:
    req_id = payload.get("id")
    method = payload.get("method")
    params = payload.get("params", [])

    if not method:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32600, "message": "Invalid Request: missing method"},
        }

    try:
        result = await dispatch_rpc_method(method, params)
        return {"jsonrpc": "2.0", "id": req_id, "result": result}
    except HTTPException as he:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32000, "message": he.detail},
        }
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32603, "message": f"Internal error: {str(e)}"},
        }


async def dispatch_rpc_method(method: str, params: List[Any]) -> Any:
    """Dispatches Ethereum RPC methods to simulated EVM state handlers."""
    
    # 1. Network & Chain Meta
    if method == "eth_chainId":
        return to_hex(CHAIN_ID)

    if method == "net_version":
        return str(CHAIN_ID)

    if method == "eth_blockNumber":
        return to_hex(CURRENT_BLOCK)

    # 2. Gas & Pricing
    if method == "eth_gasPrice":
        # Simulate realistic 20-35 Gwei gas price fluctuation
        gwei = random.randint(20, 35)
        return to_hex(gwei * 10**9)

    if method == "eth_estimateGas":
        # Standard transfer = 21,000 (0x5208)
        # Contract interaction = 120,000 (0x1d4c0)
        return "0x5208"

    # 3. Account State
    if method == "eth_getBalance":
        if not params:
            raise HTTPException(status_code=400, detail="Missing address parameter")
        addr = normalize_address(params[0])
        balance = BALANCES.get(addr, 50 * 10**18)  # Default 50 ETH for test addresses
        return to_hex(balance)

    if method == "eth_getTransactionCount":
        # Nonce retrieval
        if not params:
            raise HTTPException(status_code=400, detail="Missing address parameter")
        addr = normalize_address(params[0])
        nonce = NONCES.get(addr, 0)
        return to_hex(nonce)

    # 4. Smart Contract Calls (Simulation: ERC-20 & AMM Reserves)
    if method == "eth_call":
        # Simulate read-only EVM smart contract execution
        call_obj = params[0] if params else {}
        data = call_obj.get("data", "")

        # ERC-20 balanceOf(address) selector: 0x70a08231
        if data.startswith("0x70a08231"):
            token_balance = 10_000 * 10**18  # 10,000 Mock Tokens
            return f"0x{token_balance:064x}"

        # AMM getReserves() selector: 0x0902f1ac
        if data.startswith("0x0902f1ac"):
            # Return reserve0 (32 bytes), reserve1 (32 bytes), blockTimestamp (32 bytes)
            r0 = f"{AMM_RESERVE_WETH:064x}"
            r1 = f"{AMM_RESERVE_USDC:064x}"
            ts = f"{int(time.time()):064x}"
            return f"0x{r0}{r1}{ts}"

        # Default fallback: return 32-byte 1
        return f"0x{'0'*63}1"

    # 5. Transaction Submissions (Mempool & Nonce validation)
    if method in ("eth_sendTransaction", "eth_sendRawTransaction"):
        # Simulate transaction ingestion latency (2ms - 15ms)
        await asyncio.sleep(random.uniform(0.002, 0.015))

        if method == "eth_sendRawTransaction":
            raw_tx = params[0] if params else ""
            tx_hash = f"0x{hashlib.sha256((raw_tx + str(time.time()) + str(random.random())).encode()).hexdigest()}"
            sender = "0x" + tx_hash[2:42]
            to_addr = "0x" + hashlib.md5(raw_tx.encode()).hexdigest() + "00000000"
            nonce = NONCES.get(sender, 0)
        else:
            tx_obj = params[0] if params else {}
            sender = normalize_address(tx_obj.get("from", "0x0000000000000000000000000000000000000001"))
            to_addr = normalize_address(tx_obj.get("to", "0x0000000000000000000000000000000000000002"))
            nonce = int(str(tx_obj.get("nonce", NONCES.get(sender, 0))), 16) if isinstance(tx_obj.get("nonce"), str) and tx_obj.get("nonce").startswith("0x") else int(tx_obj.get("nonce", NONCES.get(sender, 0)))
            tx_hash = f"0x{hashlib.sha256((sender + str(nonce) + str(time.time()) + str(random.random())).encode()).hexdigest()}"

        # Nonce validation check under concurrency
        current_nonce = NONCES.get(sender, 0)
        if nonce < current_nonce:
            raise HTTPException(
                status_code=400,
                detail=f"nonce too low: address {sender}, tx: {nonce} state: {current_nonce}",
            )

        # Update sender nonce and place into mempool
        NONCES[sender] = max(current_nonce, nonce) + 1
        MEMPOOL[tx_hash] = {
            "hash": tx_hash,
            "from": sender,
            "to": to_addr,
            "nonce": nonce,
            "submitted_at": time.time(),
        }
        return tx_hash

    # 6. Receipts & Block Queries
    if method == "eth_getTransactionReceipt":
        tx_hash = params[0] if params else ""
        # If still in mempool, receipt is null (pending)
        if tx_hash in MEMPOOL:
            return None
        return RECEIPTS.get(tx_hash, None)

    if method == "eth_getBlockByNumber":
        block_num = params[0] if params else to_hex(CURRENT_BLOCK)
        num_val = int(block_num, 16) if block_num.startswith("0x") else CURRENT_BLOCK
        return {
            "number": to_hex(num_val),
            "hash": f"0x{hashlib.sha256(str(num_val).encode()).hexdigest()}",
            "parentHash": f"0x{hashlib.sha256(str(num_val - 1).encode()).hexdigest()}",
            "timestamp": to_hex(int(time.time())),
            "gasLimit": "0x1c9c380",  # 30,000,000 gas limit
            "gasUsed": "0x52080",
            "transactions": list(RECEIPTS.keys())[:10],
        }

    # Fallback for other standard methods
    return "0x0"


# ---------------------------------------------------------------------------
# AMM DEX Constant Product Swap Simulation (x * y = k)
# ---------------------------------------------------------------------------
class SwapRequest(BaseModel):
    token_in: str  # "WETH" or "USDC"
    amount_in: float
    min_amount_out: float
    trader: str


@app.post("/api/v1/dex/swap", tags=["DEX"])
async def execute_dex_swap(req: SwapRequest):
    """
    Simulates a Uniswap v2 AMM swap with Slippage & MEV Front-running risks.
    Calculates exact output via constant product formula: (x + dx) * (y - dy) = k
    """
    global AMM_RESERVE_WETH, AMM_RESERVE_USDC

    async with amm_mutex:
        if req.token_in == "WETH":
            # Swapping WETH for USDC
            dx = int(req.amount_in * 10**18)
            # Fee: 0.3% -> dx_with_fee = dx * 997
            dx_with_fee = dx * 997
            numerator = dx_with_fee * AMM_RESERVE_USDC
            denominator = (AMM_RESERVE_WETH * 1000) + dx_with_fee
            dy = numerator // denominator

            amount_out = dy / 10**6  # USDC 6 decimals

            # Slippage check
            if amount_out < req.min_amount_out:
                raise HTTPException(
                    status_code=400,
                    detail=f"Slippage Error: Expected at least {req.min_amount_out} USDC, but received {amount_out:.2f} USDC (Price Impact / Frontrun detected)",
                )

            AMM_RESERVE_WETH += dx
            AMM_RESERVE_USDC -= dy

            tx_hash = f"0x{hashlib.sha256(f'swap_{time.time()}_{random.random()}'.encode()).hexdigest()}"
            return {
                "status": "SUCCESS",
                "tx_hash": tx_hash,
                "token_in": "WETH",
                "amount_in": req.amount_in,
                "amount_out": round(amount_out, 2),
                "token_out": "USDC",
                "new_reserve_weth": AMM_RESERVE_WETH / 10**18,
                "new_reserve_usdc": AMM_RESERVE_USDC / 10**6,
                "execution_price": round(amount_out / req.amount_in, 2),
            }
        else:
            # Swapping USDC for WETH
            dx = int(req.amount_in * 10**6)
            dx_with_fee = dx * 997
            numerator = dx_with_fee * AMM_RESERVE_WETH
            denominator = (AMM_RESERVE_USDC * 1000) + dx_with_fee
            dy = numerator // denominator

            amount_out = dy / 10**18

            if amount_out < req.min_amount_out:
                raise HTTPException(
                    status_code=400,
                    detail=f"Slippage Error: Expected at least {req.min_amount_out} WETH, but received {amount_out:.4f} WETH",
                )

            AMM_RESERVE_USDC += dx
            AMM_RESERVE_WETH -= dy

            tx_hash = f"0x{hashlib.sha256(f'swap_{time.time()}_{random.random()}'.encode()).hexdigest()}"
            return {
                "status": "SUCCESS",
                "tx_hash": tx_hash,
                "token_in": "USDC",
                "amount_in": req.amount_in,
                "amount_out": round(amount_out, 4),
                "token_out": "WETH",
                "new_reserve_weth": AMM_RESERVE_WETH / 10**18,
                "new_reserve_usdc": AMM_RESERVE_USDC / 10**6,
                "execution_price": round(req.amount_in / amount_out, 2),
            }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8545, log_level="warning")
