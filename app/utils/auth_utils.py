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


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Creates a time-limited JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
        
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    """Decodes and validates a JWT."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
