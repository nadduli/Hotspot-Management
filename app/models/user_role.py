#!/usr/bin/python3
"""
Docstring for app.models.user_role - Association table for User <-> Role (RBAC).
"""

import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from app.db.base import BaseModel # Inherits created_at/updated_at


class UserRole(BaseModel):
    """
    Junction table linking Users to Roles.
    It uses a composite primary key composed of user_id and role_id.
    """

    __tablename__ = "user_roles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), 
        primary_key=True
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("roles.id"), 
        primary_key=True
    )