#!/usr/bin/python3
"""
Docstring for app.models.roles
"""
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from sqlalchemy import String
from app.db.base import BaseModel


class Role(BaseModel):
    """
    Docstring for Role
    """

    __tablename__ = "roles"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(50), unique=True)

    users = relationship("User", secondary="user_roles", back_populates="roles")
