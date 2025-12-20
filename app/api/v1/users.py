#!/usr/bin/python3
"""
Users API Endpoints
"""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_db, get_current_admin_user
from app.schemas.auth import UserCreate
from app.services.auth_service import AuthService
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=dict)
async def create_agent(
    user_in: UserCreate,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Create a new Agent in the current user's organization.
    Only ADMINs can perform this action.
    """
    # Check if user exists
    result = await db.execute(select(User).where(User.email == user_in.email))
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    auth_service = AuthService(db)
    # Create user with AGENT role in the same organization as the admin
    user = await auth_service.create_user(
        user_in, organization_id=current_user.organization_id, role_name="AGENT"
    )

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": "AGENT",
        "organization_id": user.organization_id,
    }
