import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_user_registration(client: AsyncClient):
    user_data = {
        "email": "newuser@example.com",
        "password": "StrongPassword123!",
        "confirm_password": "StrongPassword123!",
        "full_name": "Test User"
    }

    response = await client.post("/api/v1/auth/register", json=user_data)
    if response.status_code == 422:
        print(response.json())
    assert response.status_code == 201
    
    json_response = response.json()
    user_info = json_response["data"] 

    assert user_info["email"] == "newuser@example.com"
    assert "id" in user_info
    assert "password" not in user_info