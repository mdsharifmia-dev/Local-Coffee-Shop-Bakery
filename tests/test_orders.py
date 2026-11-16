import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_order_atomic_success(client: AsyncClient):
    payload = {
        "customer_name": "Test Customer",
        "customer_phone": "+15551234567",
        "payment_method": "Cash on Delivery / Counter",
        "special_notes": "Extra hot",
        "items": [
            {"menu_item_id": 1, "quantity": 2},  # Espresso ($3.50 * 2 = $7.00)
            {"menu_item_id": 7, "quantity": 1},  # Croissant ($3.00 * 1 = $3.00)
        ],
    }
    response = await client.post("/api/orders", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["order_code"].startswith("ORD-")
    assert data["customer_name"] == "Test Customer"
    assert data["total_price"] == 10.00
    assert data["status"] == "pending"
    assert len(data["items"]) == 2

    # Track order via code
    order_code = data["order_code"]
    track_resp = await client.get(f"/api/orders/{order_code}")
    assert track_resp.status_code == 200
    assert track_resp.json()["id"] == data["id"]


@pytest.mark.asyncio
async def test_create_order_invalid_item_fails(client: AsyncClient):
    payload = {
        "customer_name": "Error Test",
        "payment_method": "bKash",
        "items": [{"menu_item_id": 99999, "quantity": 1}],
    }
    response = await client.post("/api/orders", json=payload)
    assert response.status_code == 400
    assert "does not exist" in response.json()["detail"]
