#!/usr/bin/python3
"""
Docstring for app.db.org_base - Enforces multi-tenancy by linking records
to a parent Organization.
"""

import uuid
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy import ForeignKey
from .base import BaseModel


class OrgBaseModel(BaseModel):
    """
    Abstract model adding a UUID primary key and a mandatory organization_id
    Foreign Key for multi-tenancy.
    """

    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True, nullable=False
    )

    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id"), index=True, nullable=False
    )

