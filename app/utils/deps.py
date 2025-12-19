#!/usr/bin/python3
"""
Docstring for app.utils.deps
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from app.db.session import get_db
from app.models.user import User
from app.utils.auth_utils import decode_access_token
from app.schemas.auth import UserRoleEnum
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_user(
        db: AsyncSession = Depends(get_db),
        token: str = Depends(oauth2_scheme)
) -> User:
    """
    Authenticates the user by validating the JWT and fetching the user object
    """
    payload = decode_access_token(token)
    user_id = payload.get("user_id")

    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    user_result = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
    user: User | None = user_result.scalar_one_or_none()

    if user is None or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not Found or not active")
    
    return user


class RoleChecker:
    """
    Dependency to check if the current user has at least one of the required roles.
    Usage: Depends(RoleChecker([UserRoleEnum.SUPER_ADMIN, UserRoleEnum.VENUE_OWNER]))
    """
    def __init__(self, allowed_roles: list[UserRoleEnum]):
        self.allowed_roles = [role.value for role in allowed_roles]

    async def __call__(self, user: User = Depends(get_current_user)):
        user_roles = [role.name for role in user.roles]
    
        if not set(self.allowed_roles).intersection(set(user_roles)):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient user privileges.",
            )
        return user