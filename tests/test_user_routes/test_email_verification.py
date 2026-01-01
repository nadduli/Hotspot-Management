#!/usr/bin/python3
"""Test Email Verification"""

import pytest
from unittest.mock import AsyncMock, patch
from app.models.user import User
from app.services.token_service import create_verification_token
from app.core.security import hash_password

@pytest.mark.asyncio
async def test_registration_sends_email(client, db_session):
    """Test that registration triggers an email send"""
    with patch("app.services.auth_service.EmailService.send_verification_email", new_callable=AsyncMock) as mock_send:
        payload = {
            "full_name": "Test Email User",
            "email": "test_email@example.com",
            "password": "Password123!",
            "confirm_password": "Password123!"
        }
        response = await client.post("/api/v1/auth/register", json=payload)
        assert response.status_code == 201
        
        mock_send.assert_called_once()
        args, _ = mock_send.call_args
        assert isinstance(args[0], User)
        assert args[0].email == "test_email@example.com"
        assert isinstance(args[1], str)


@pytest.mark.asyncio
async def test_verify_email_success(client, db_session):
    """Test successful email verification"""
    user = User(
        full_name="Verify User",
        email="verify@example.com",
        email_verified=False,
        password_hash=hash_password("Pass123!")
    )
    user.add(db_session)
    await db_session.commit()
    await db_session.refresh(user)
    
    token = create_verification_token(user.email)
    
    response = await client.get(f"/api/v1/auth/verify-email?token={token}")
    assert response.status_code == 200
    assert response.json()["message"] == "Email verified successfully"
    
    await db_session.refresh(user)
    assert user.email_verified is True


@pytest.mark.asyncio
async def test_verify_email_invalid_token(client):
    """Test verification with invalid token"""
    response = await client.get("/api/v1/auth/verify-email?token=invalid_token")
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid or expired token"

@pytest.mark.asyncio
async def test_verify_email_already_verified(client, db_session):
    """Test verifying an already verified user"""
    user = User(
        full_name="Verified User",
        email="verified@example.com",
        email_verified=True,
        password_hash=hash_password("Pass123!")
    )
    user.add(db_session)
    await db_session.commit()
    await db_session.refresh(user)
    
    token = create_verification_token(user.email)
    
    response = await client.get(f"/api/v1/auth/verify-email?token={token}")
    assert response.status_code == 200
