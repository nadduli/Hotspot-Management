#!/usr/bin/python3
"""Token Schema"""

from pydantic import BaseModel


class Token(BaseModel):
    """Schema for authentication token"""
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Schema for token payload"""
    sub: str | None = None
