import time
import pytest
from httpx import AsyncClient
from app.core.rate_limiter import rate_limiter


@pytest.mark.asyncio
async def test_rate_limiter_allows_and_blocks(client: AsyncClient):
    test_ip = "192.168.1.100"
    rate_limiter.reset_for_ip(test_ip)

    # 1. First request should be allowed
    resp = await client.get("/api/menu", headers={"X-Forwarded-For": test_ip})
    assert resp.status_code == 200
    assert "X-RateLimit-Limit" in resp.headers

    # 2. Simulate exhausting the quota within current time window
    now = time.time()
    rate_limiter.requests_map[test_ip] = [now] * rate_limiter.max_requests

    resp_blocked = await client.get("/api/menu", headers={"X-Forwarded-For": test_ip})
    assert resp_blocked.status_code == 429
    assert "Retry-After" in resp_blocked.headers
    assert "Rate limit exceeded" in resp_blocked.json()["detail"]

    # Reset after test
    rate_limiter.reset_for_ip(test_ip)
