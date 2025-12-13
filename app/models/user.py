#!/usr/bin/python3
"""
Docstring for app.models.user
"""

import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey, Text
from app.db.org_base import OrgBaseModel


class User(OrgBaseModel):
    """
    Docstring for User
    """

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str | None] = mapped_column(String(150), unique=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(20), unique=True)
    password_hash: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    roles = relationship("Role", secondary="user_roles", back_populates="users")
