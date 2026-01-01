#!/usr/bin/python3
"""token service module"""

from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from fastapi import HTTPException, status
from app.core.config import get_settings


settings = get_settings()


serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_verification_token(email:str):
    """create email token"""
    return serializer.dumps(email, salt=settings.SECURITY_SALT)

def verify_registration_token(token: str, expiration: int = 3600):
    """verify token"""
    try:
        return serializer.loads(
            token,
            salt=settings.SECURITY_SALT,
            max_age=expiration
        )
    except SignatureExpired:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except BadSignature:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")