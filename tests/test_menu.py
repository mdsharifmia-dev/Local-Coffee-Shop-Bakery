import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_menu_items(client: AsyncClient):
    response = await client.get("/api/menu")
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert len(items) >= 12

    # Validate structure
    first = items[0]
    assert "id" in first
    assert "name" in first
    assert "price" in first
    assert "category" in first


@pytest.mark.asyncio
async def test_menu_caching_and_categories(client: AsyncClient):
    # First call warms cache
    resp1 = await client.get("/api/menu?category=coffee")
    assert resp1.status_code == 200
    coffee_items = resp1.json()
    assert all(item["category"] == "coffee" for item in coffee_items)

    # Second call should be a cache HIT
    resp2 = await client.get("/api/menu?category=coffee")
    assert resp2.status_code == 200
    assert resp2.headers.get("X-Cache-Status") == "HIT"

    # Category pastry
    resp3 = await client.get("/api/menu?category=pastry")
    assert resp3.status_code == 200
    pastry_items = resp3.json()
    assert all(item["category"] == "pastry" for item in pastry_items)
