#!/usr/bin/python3
"""Test Login Endpoint"""

import pytest
from httpx import AsyncClient
from app.models.user import User
from app.core.security import hash_password

@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, db_session):
    """Test successful login returns token"""
    # Create user
    password = "StrongPassword123!"
    user = User(
        full_name="Login User",
        email="login@example.com",
        email_verified=True,
        password_hash=hash_password(password)
    )
    user.add(db_session)
    await db_session.commit()
    
    # Login
    login_data = {"email": "login@example.com", "password": password}
    response = await client.post("/api/v1/auth/login", json=login_data)
    
    assert response.status_code == 200
    data = response.json()["data"]
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient, db_session):
    """Test login with wrong password"""
    # Create user
    password = "StrongPassword123!"
    user = User(
        full_name="Login User",
        email="login_fail@example.com",
        email_verified=True,
        password_hash=hash_password(password)
    )
    user.add(db_session)
    await db_session.commit()
    
    # Wrong Password
    login_data = {"email": "login_fail@example.com", "password": "WrongPassword"}
    response = await client.post("/api/v1/auth/login", json=login_data)
    
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["message"]

@pytest.mark.asyncio
async def test_login_user_not_found(client: AsyncClient):
    """Test login with non-existent user"""
    login_data = {"email": "notfound@example.com", "password": "Password123!"}
    response = await client.post("/api/v1/auth/login", json=login_data)
    
    assert response.status_code == 401
    # Security best practice: don't reveal if user exists. We use same message.
    assert "Incorrect email or password" in response.json()["message"]

@pytest.mark.asyncio
async def test_swagger_login(client: AsyncClient, db_session):
    """Test standard OAuth2 form login"""
    password = "StrongPassword123!"
    user = User(
        full_name="Swagger User",
        email="swagger@example.com",
        email_verified=True,
        password_hash=hash_password(password)
    )
    user.add(db_session)
    await db_session.commit()
    
    # Form data
    form_data = {"username": "swagger@example.com", "password": password}
    response = await client.post("/api/v1/auth/token", data=form_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
