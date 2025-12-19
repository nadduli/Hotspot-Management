#!/usr/bin/python3
"""
Docstring for app.models.__init__ - Initialize models.
"""
from .user import User
from .roles import Role
from .user_role import UserRole
from .organization import Organization
from .branch import Branch



__all__ = [
    "User",
    "Role",
    "UserRole",
    "Organization",
    "Branch",
]