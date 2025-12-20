#!/usr/bin/python3
"""
Docstring for app.schemas.auth
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from enum import Enum as PyEnum
import uuid


class UserRoleEnum(str, PyEnum):
    """
    Docstring for UserRoleEnum
    """

    ADMIN = "ADMIN"
    AGENTS = "AGENTS"


class UserCreate(BaseModel):
    """
    Docstring for UserCreate
    """

    name: str = Field(..., max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    phone: Optional[str] = None
    role: Optional[UserRoleEnum] = UserRoleEnum.ADMIN


class Token(BaseModel):
    """
    Docstring for Token
    """

    access_token: str
    token_type: str = "bearer"
    expires_in: int
