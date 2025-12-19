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
    """
    Represents a specific physical hotspot location.
    """

    __tablename__ = "branches"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(
        String(255), unique=True, nullable=True
    )

    # Override organization to specify back_populates
    organization: Mapped["Organization"] = relationship("Organization", back_populates="branches")

    def __repr__(self) -> str:
        return f"<Branch(id={self.id}, name={self.name}, organization_id={self.organization_id})>"
