"""
Mock E-Commerce REST API for SDET Performance Testing.
Simulates realistic API latency, authentication, and order processing.
"""
import asyncio
import random
import time
import uuid
from typing import Optional

from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel

app = FastAPI(
    title="SDET Mock E-Commerce API",
    description="High-performance mock API designed for load and performance benchmarking.",
    version="1.0.0",
)

# In-memory session store
VALID_USERS = {
    "admin": "admin123",
    "testuser": "password123",
    "perf_tester": "secret_perf_2026",
}
ACTIVE_TOKENS = set()

# Mock Products catalog
PRODUCTS = [
    {"id": f"PROD-{i:04d}", "name": f"High-Performance Laptop Gen {i}", "price": 999.0 + i * 15, "stock": 100}
    for i in range(1, 101)
]


class LoginRequest(BaseModel):
    username: str
    password: str


class OrderItem(BaseModel):
    product_id: str
    quantity: int


class OrderRequest(BaseModel):
    items: list[OrderItem]
    shipping_address: Optional[str] = "123 SDET Performance Way"


@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint for CI/CD readiness probes."""
    return {"status": "healthy", "timestamp": time.time()}


@app.post("/api/v1/auth/login", tags=["Authentication"])
async def login(req: LoginRequest):
    """
    Authenticate user and issue a Bearer token.
    Simulates database lookup and cryptographic hashing latency (30ms - 80ms).
    """
    await asyncio.sleep(random.uniform(0.03, 0.08))

    # Accept either registered users or any username starting with 'perf_' or 'user_'
    is_valid = (
        VALID_USERS.get(req.username) == req.password
        or req.username.startswith("perf_")
        or req.username.startswith("user_")
    )

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = f"sdet_jwt_{uuid.uuid4().hex}"
    ACTIVE_TOKENS.add(token)

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": 3600,
        "user": req.username,
    }


@app.get("/api/v1/products", tags=["Catalog"])
async def get_products(
    limit: int = 10,
    category: Optional[str] = None,
    authorization: Optional[str] = Header(None),
):
    """
    Retrieve products catalog.
    Simulates cache miss / database query latency (40ms - 100ms).
    """
    await asyncio.sleep(random.uniform(0.04, 0.10))

    # Optional 1% simulated transient timeout under peak load
    if random.random() < 0.005:
        await asyncio.sleep(0.3)

    return {
        "total": len(PRODUCTS),
        "limit": limit,
        "products": PRODUCTS[:limit],
    }


@app.post("/api/v1/orders", tags=["Orders"])
async def create_order(order: OrderRequest, authorization: Optional[str] = Header(None)):
    """
    Place a new customer order.
    Requires Authorization header. Simulates transactional latency (80ms - 180ms).
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or malformed Authorization header",
        )

    # Process order
    await asyncio.sleep(random.uniform(0.08, 0.18))

    order_id = f"ORD-{int(time.time())}-{random.randint(1000, 9999)}"
    total_amount = sum(item.quantity * 99.0 for item in order.items)

    return {
        "order_id": order_id,
        "status": "CONFIRMED",
        "items_count": len(order.items),
        "total_amount": round(total_amount, 2),
        "created_at": time.time(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False, workers=2)
