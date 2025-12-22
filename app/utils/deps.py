from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt, JWTError
import uuid
from app.db.session import get_db
from app.models.user import User
from app.models.blacklist import TokenBlacklist
from app.core.config import get_settings

settings = get_settings()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    """
    Async dependency to retrieve the current authenticated user.

    Raises 401 if:
    - Token is missing, invalid, expired, or revoked
    - JWT payload is malformed
    - User not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if await TokenBlacklist.is_token_blacklisted(db, token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("token_type") != "access":
            raise credentials_exception

        user_data = payload.get("user")
        if not user_data:
            raise credentials_exception

        user_id = user_data.get("user_id")
        if not user_id:
            raise credentials_exception

    except JWTError:
        raise credentials_exception
    
    try:
        user_id_uuid = uuid.UUID(user_id)
    except (ValueError, AttributeError):
        raise credentials_exception

    statement = select(User).where(User.id == user_id_uuid)
    result = await db.execute(statement)
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user


def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

def require_agent_or_admin(user: User = Depends(get_current_user)) -> User:
    if user.role.name not in {"admin", "agent"}:
        raise HTTPException(status_code=403)
    return user
