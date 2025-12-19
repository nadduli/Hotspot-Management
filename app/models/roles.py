#!/usr/bin/python3
"""
Docstring for app.models.roles - Defines roles for RBAC.
"""
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from sqlalchemy import String
from app.db.base import BaseModel
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User

class Role(BaseModel):
    """
    Represents a system role (e.g., SUPER_ADMIN, VENUE_OWNER).
    """

    __tablename__ = "roles"
    
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(50), unique=True)

    users: Mapped[List["User"]] = relationship(
        secondary="user_roles", 
        back_populates="roles"
    )