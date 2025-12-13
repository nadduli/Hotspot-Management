#!/usr/bin/python3
"""
Docstring for app.models.user_role
"""

import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from app.db.base import BaseModel


class UserRole(BaseModel):
    """
    Docstring for UserRole
    """

    __tablename__ = "user_roles"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True, nullable=False
    )
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    role_id: Mapped[str] = mapped_column(ForeignKey("roles.id"))
