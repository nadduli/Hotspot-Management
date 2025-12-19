#!/usr/bin/python3
"""
Docstring for app.models.user - User Account model.
"""

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean
from app.db.org_base import OrgBaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.roles import Role
    from app.models.organization import Organization


class User(OrgBaseModel):
    """
    Represents a user account within the system.
    """

    __tablename__ = "users"
    
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str | None] = mapped_column(String(150), unique=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(20), unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    roles: Mapped[list["Role"]] = relationship("Role", secondary="user_roles", back_populates="users")
    
    # Override organization to specify back_populates
    organization: Mapped["Organization"] = relationship("Organization", back_populates="users")