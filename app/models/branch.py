#!/usr/bin/python3
"""
Docstring for app.models.branch - Physical Hotspot Location model.
"""
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from sqlalchemy.orm import relationship
from app.db.base_model import BaseModel
from typing import Optional
from sqlalchemy import ForeignKey
from .organization import Organization


class Branch(BaseModel):
    __tablename__ = "branches"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), index=True)
    address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))

    organization: Mapped["Organization"] = relationship(back_populates="branches")
    users: Mapped[list["User"]] = relationship(back_populates="branch")
