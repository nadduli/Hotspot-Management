#!/usr/bin/python3
"""User model definition."""
from __future__ import annotations
from datetime import datetime
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, String, ForeignKey, DateTime
from app.db.base_model import BaseModel


class User(BaseModel):
    """User model representing system users."""

    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True, nullable=False
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(255))
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime)

    role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("roles.id"))
    branch_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("branches.id"))

    role: Mapped["Role"] = relationship("Role", back_populates="users", lazy="selectin")  # type: ignore
    branch: Mapped["Branch"] = relationship("Branch", back_populates="users")  # type: ignore
