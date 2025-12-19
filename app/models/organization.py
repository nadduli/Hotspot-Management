#!/usr/bin/python3
"""
Docstring for app.models.organization - Organization (Tenant) model.
"""
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import BaseModel
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
    address: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(
        String(255), unique=True, nullable=True
    )
    currency: Mapped[Optional[str]] = mapped_column(
        String(10), nullable=True, default="UGX"
    )

    users = relationship("User", back_populates="organization")
    branches = relationship("Branch", back_populates="organization")


    def __repr__(self) -> str:
        return f"<Organization(id={self.id}, name={self.name})>"
