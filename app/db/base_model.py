#!/usr/bin/python3
"""Base model with common fields and methods for all database models"""
from datetime import datetime, timezone
from sqlalchemy import DateTime, select
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession


class Base(DeclarativeBase):
    """Base class for all models"""

    pass


class BaseModel(Base):
    """Abstract base model with common fields and methods"""

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def add(self, db: AsyncSession):
        """Add object to session locally"""
        db.add(self)
        return self

    def remove(self, db: AsyncSession):
        """Mark object for deletion locally"""
        db.delete(self)
        return self

    async def insert(self, db: AsyncSession, commit: bool = True):
        """Insert new object to db"""
        db.add(self)
        if commit:
            await db.commit()
            await db.refresh(self)
        return self

    async def update(self, db: AsyncSession, commit: bool = True, **kwargs):
        """Update specific fields and save to db"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

        if commit:
            await db.commit()
            await db.refresh(self)
        return self

    async def delete(self, db: AsyncSession, commit: bool = True) -> None:
        """Delete object from db"""
        await db.delete(self)
        if commit:
            await db.commit()

    @classmethod
    async def fetch_one(cls, db: AsyncSession, **kwargs):
        """Get first matching object"""
        query = select(cls).filter_by(**kwargs)
        result = await db.execute(query)
        return result.scalars().first()

    @classmethod
    async def fetch_unique(cls, db: AsyncSession, **kwargs):
        """Get unique object or None (raises error if multiple found)"""
        query = select(cls).filter_by(**kwargs)
        result = await db.execute(query)
        return result.scalars().one_or_none()

    @classmethod
    async def fetch_all(cls, db: AsyncSession, **kwargs):
        """Get all matching objects"""
        query = select(cls).filter_by(**kwargs)
        result = await db.execute(query)
        return list(result.scalars().all())
