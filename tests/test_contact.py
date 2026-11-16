import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_contact_submission_success(client: AsyncClient):
    payload = {
        "name": "Jane Developer",
        "email": "jane@example.com",
        "subject": "Coffee Bean Wholesale",
        "message": "We would like to discuss wholesale coffee supply for our cafe.",
    }
    response = await client.post("/api/contact", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert "received" in data["message"].lower()


@pytest.mark.asyncio
async def test_contact_submission_invalid_email(client: AsyncClient):
    payload = {
        "name": "Jane Developer",
        "email": "not-an-email",
        "subject": "Coffee Bean Wholesale",
        "message": "Short message.",
    }
    response = await client.post("/api/contact", json=payload)
    assert response.status_code == 422
