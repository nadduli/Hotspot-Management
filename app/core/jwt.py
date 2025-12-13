#!/usr/bin/python3
"""
Docstring for app.core.jwt - JSON Web Token Utilities
"""

from datetime import datetime, timedelta, timezone
from jose import jwt
from .config import get_settings
from typing import Optional, Any

settings = get_settings()

SECRET_KEY: str = settings.SECRET_KEY
ALGORITHM: str = settings.ALGORITHM


def create_access_token(
    data: dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Creates a JWT access token with a configurable expiration time.
    Uses timezone-aware UTC timestamps.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire.timestamp()})

    to_encode.update({"iat": datetime.now(timezone.utc).timestamp()})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
