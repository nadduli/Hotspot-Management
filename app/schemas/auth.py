#!/usr/bin/python3
"""
Docstring for app.schemas.auth
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    """
    Docstring for UserCreate
    """

    name: str = Field(..., max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    phone: Optional[str] = None


class Token(BaseModel):
    """
    Docstring for Token
    """

    access_token: str
    token_type: str = "bearer"
    expires_in: int
