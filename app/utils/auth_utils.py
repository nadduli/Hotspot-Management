#!/usr/bin/python3
"""
Docstring for app.core.jwt - JSON Web Token Utilities
"""

from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from ..core.config import get_settings
from fastapi import HTTPException, status


settings = get_settings()

SECRET_KEY: str = settings.SECRET_KEY
ALGORITHM: str = settings.ALGORITHM


def create_access_token(user_id, role: str) -> str:
    """Creates a time-limited JWT."""
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=30),
        "token_type": "access",
        }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token

def create_refresh_token(user_id, role: str) -> str:
    """Creates a time-limited JWT for refreshing access tokens."""
    user = {
        "user_id": str(user_id),
        "role": role,
    }
    payload = {
        "user": user,
        "exp": datetime.now(tz=timezone.utc) + timedelta(days=7),
        "token_type": "refresh",
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token

def generate_refresh_token(subject: str, role: str = "admin") -> str:
    """compatibility wrapper used by tests and older code
    Accepts subject as str, but uses user_id in the payload
    """
    user_id = str(subject) if subject is not None else ""
    return create_refresh_token(user_id, role)

    
def decode_access_token(token: str) -> dict:
    """Decodes and validates a JWT."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
