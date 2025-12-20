import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_root(async_client: AsyncClient):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


@pytest.mark.anyio
async def test_health(async_client: AsyncClient):
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# Note: These tests require a running DB with seeded roles.
# In a real CI environment, we would use a test DB.
# For now, we are assuming the environment is set up or these will be skipped/fail gracefully if not.


@pytest.mark.anyio
async def test_register_admin_flow(async_client: AsyncClient):
    # 1. Register as Admin
    payload = {
        "name": "Admin User",
        "email": "admin@example.com",
        "password": "password123",
        "phone": "1234567890",
    }
    # This might fail if user exists, so we handle 400
    response = await async_client.post("/api/v1/auth/register", json=payload)
    if response.status_code == 400:
        # User exists, try login
        login_payload = {"username": payload["email"], "password": payload["password"]}
        response = await async_client.post("/api/v1/auth/login", data=login_payload)

    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Verify Role (via /me or by creating agent)
    me_response = await async_client.get("/api/v1/auth/me", headers=headers)
    assert me_response.status_code == 200
    # Note: /me response doesn't currently return roles, but we can infer permissions by next step

    # 3. Create Agent
    agent_payload = {
        "name": "Agent User",
        "email": "agent@example.com",
        "password": "password123",
        "phone": "0987654321",
    }
    agent_response = await async_client.post(
        "/api/v1/users/", json=agent_payload, headers=headers
    )

    if agent_response.status_code == 400:
        # Agent might exist
        pass
    else:
        assert agent_response.status_code == 200
        assert agent_response.json()["role"] == "AGENT"
