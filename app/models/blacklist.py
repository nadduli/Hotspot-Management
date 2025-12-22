#!/usr/bin/python3
"""
Docstring for app.models.blacklist
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Text, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_model import BaseModel


class TokenBlacklist(BaseModel):
    """
    Model representing a blacklisted (revoked) JWT token.
    """

    __tablename__ = "token_blacklist"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    token: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    token_type: Mapped[str] = mapped_column(String(50), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(nullable=False, index=True)
    reason: Mapped[str | None] = mapped_column(String(200))

    @classmethod
    def is_token_blacklisted(cls, db, token: str) -> bool:
        """Check if token is blacklisted"""
        blacklisted_token = cls.fetch_unique(db, token=token)
        return blacklisted_token is not None

    @classmethod
    def cleanup_expired_tokens(cls, db):
        """Remove expired tokens from blacklist using BaseModel methods"""
        expired_tokens = cls.fetch_all(db)
        expired_count = 0
        
        for token in expired_tokens:
            if token.expires_at < datetime.now(timezone.utc):
                token.delete(db)
                expired_count += 1
                
        return expired_count