"""
Product Hunt Launch Spike Load Tester.
Executes high-concurrency burst tests against MVP endpoints to evaluate free-tier backend resilience.
"""
import asyncio
import math
import time
from typing import Dict, List

import httpx


def calculate_percentile(values: List[float], pct: float) -> float:
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    k = (len(sorted_vals) - 1) * (pct / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return float(sorted_vals[int(k)])
    return float(sorted_vals[int(f)] * (c - k) + sorted_vals[int(c)] * (k - f))


async def run_spike_test(
    target_url: str,
    virtual_users: int = 30,
    burst_duration_sec: int = 8,
) -> Dict:
    """Fires concurrent requests against target MVP to assess server stability under traffic spikes."""
    latencies = []
    status_codes = []
    t_start = time.time()
    total_dispatched = 0

    limits = httpx.Limits(max_keepalive_connections=virtual_users, max_connections=virtual_users * 2)
    async with httpx.AsyncClient(limits=limits, timeout=10.0, follow_redirects=True) as client:
        async def worker():
            nonlocal total_dispatched
            while time.time() - t_start < burst_duration_sec:
                req_t0 = time.perf_counter()
                try:
                    res = await client.get(target_url)
                    req_elapsed = (time.perf_counter() - req_t0) * 1000
                    latencies.append(req_elapsed)
                    status_codes.append(res.status_code)
                except httpx.TimeoutException:
                    latencies.append(10000.0)
                    status_codes.append(504)
                except Exception:
                    latencies.append(5000.0)
                    status_codes.append(500)
                total_dispatched += 1
                await asyncio.sleep(0.05)

        workers = [worker() for _ in range(virtual_users)]
        await asyncio.gather(*workers)

    actual_duration = max(time.time() - t_start, 1.0)
    errors_5xx = sum(1 for c in status_codes if c >= 500)
    errors_4xx = sum(1 for c in status_codes if 400 <= c < 500)
    success_2xx = sum(1 for c in status_codes if 200 <= c < 300)

    total = len(status_codes)
    err_5xx_rate = round((errors_5xx / total * 100.0), 2) if total > 0 else 0.0
    throughput_rps = round(total / actual_duration, 1)

    p50 = round(calculate_percentile(latencies, 50), 1)
    p90 = round(calculate_percentile(latencies, 90), 1)
    p95 = round(calculate_percentile(latencies, 95), 1)
    p99 = round(calculate_percentile(latencies, 99), 1)

    # Launch Readiness Verdict
    passed = err_5xx_rate <= 1.0 and p95 <= 1500.0

    return {
        "status": "COMPLETED",
        "virtual_users": virtual_users,
        "duration_sec": round(actual_duration, 2),
        "total_requests": total,
        "throughput_rps": throughput_rps,
        "success_2xx": success_2xx,
        "errors_4xx": errors_4xx,
        "errors_5xx": errors_5xx,
        "error_5xx_rate_pct": err_5xx_rate,
        "latency_p50_ms": p50,
        "latency_p90_ms": p90,
        "latency_p95_ms": p95,
        "latency_p99_ms": p99,
        "launch_ready": passed,
    }
