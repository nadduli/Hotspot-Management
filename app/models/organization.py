#!/usr/bin/python3
"""
Docstring for app.models.organization - Organization (Tenant) model.
"""
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_model import BaseModel
from sqlalchemy import String
from typing import Optional


class Organization(BaseModel):
    """
    Represents the main tenant (Venue Owner/Hotspot Company).
    """

    __tablename__ = "organizations"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)

    branches: Mapped[list["Branch"]] = relationship(
        back_populates="organization", cascade="all, delete-orphan"
    )
