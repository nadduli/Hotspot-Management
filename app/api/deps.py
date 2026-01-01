#!/usr/bin/python3
"""Dependencies for Auth"""

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import get_settings
from app.db.session import get_db
from app.services.auth_service import AuthService
from app.models.user import User
from app.core.exceptions import AuthenticationError, UserNotFoundError
from app.schemas.token import TokenPayload

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise AuthenticationError("Could not validate credentials")
        token_data = TokenPayload(sub=username)
    except JWTError:
        raise AuthenticationError("Could not validate credentials")


    
    # Direct fetch is better here to avoid password check logic
    user = await User.fetch_unique(db, email=token_data.sub)
    if user is None:
        raise UserNotFoundError("User not found")
        
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Check if user is active"""
    if not current_user.is_active:
        raise AuthenticationError("Inactive user")
    return current_user


def get_current_user_with_role(role: str):
    """Factory to check for specific role"""
    async def _get_user_with_role(
        current_user: User = Depends(get_current_active_user)
    ) -> User:
        if current_user.role != role and current_user.role != "admin": # Admin can always access
             # Simple RBAC: Exact match or admin overrides
            raise AuthenticationError("Not enough permissions")
        return current_user
    return _get_user_with_role
