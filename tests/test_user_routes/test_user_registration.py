import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_user_registration(client: AsyncClient):
    user_data = {
        "email": "newuser@example.com",
        "password": "StrongPassword123!",
        "confirm_password": "StrongPassword123!",
        "full_name": "Test User",
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


@pytest.mark.asyncio
async def test_create_user_with_existing_email(client: AsyncClient):
    """create user with existing email should fail"""
    user_data = {
        "email": "naddulidaniel@gmail.com",
        "full_name": "Nadduli Daniel",
        "password": "StrongPassword123!",
        "confirm_password": "StrongPassword123!",
    }
    first_response = await client.post("/api/v1/auth/register", json=user_data)
    assert first_response.status_code == 201

    second_response = await client.post("/api/v1/auth/register", json=user_data)
    assert second_response.status_code == 409


@pytest.mark.asyncio
async def test_create_user_with_invalid_email(client: AsyncClient):
    """create user with invalid email should fail"""
    user_data = {
        "email": "invalid-email",
        "full_name": "Invalid Email User",
        "password": "StrongPassword123!",
        "confirm_password": "StrongPassword123!",
    }
    response = await client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code != 201
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_user_with_empty_password(client: AsyncClient):
    """create user with empty password should fail"""
    user_data = {
        "email": "",
        "full_name": "No Password User",
        "password": "StrongPassword123!",
        "confirm_password": "StrongPassword123!",
    }
    response = await client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code != 201
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_user_with_numeric_password(client: AsyncClient):
    """create user with numeric password should fail"""
    user_data = {
        "email": "test@example.com",
        "full_name": "Numeric Password User",
        "password": "123456789",
        "confirm_password": "123456789",
    }
    response = await client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code != 201
    assert response.status_code == 422
