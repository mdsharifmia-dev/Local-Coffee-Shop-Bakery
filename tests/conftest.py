import asyncio
from typing import AsyncGenerator
import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app, lifespan


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with lifespan(app):
        async with ASGITransport(app=app) as transport:
            async with AsyncClient(transport=transport, base_url="http://test") as ac:
                yield ac
