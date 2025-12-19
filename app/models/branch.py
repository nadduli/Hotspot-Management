#!/usr/bin/python3
"""
Docstring for app.models.branch - Physical Hotspot Location model.
"""
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from app.db.org_base import OrgBaseModel
from typing import Optional, TYPE_CHECKING
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from app.models.organization import Organization


class Branch(OrgBaseModel):
    __tablename__ = "branches"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True)

    organization: Mapped["Organization"] = relationship(
        "Organization", 
        back_populates="branches"
    )

    def __repr__(self) -> str:
        return f"<Branch(name={self.name})>"