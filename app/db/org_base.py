#!/usr/bin/python3
"""
Docstring for app.db.org_base
"""

import uuid
from sqlalchemy.orm import Mapped, mapped_column
from .base import BaseModel


class OrgBaseModel(BaseModel):
    """
    Docstring for OrgBaseModel
    """

    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True, nullable=False
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        default=uuid.uuid4, index=True, nullable=False
    )
