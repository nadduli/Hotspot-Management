#!/usr/bin/python3
"""
Docstring for app.db.database
"""

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator
from app.core.config import get_settings


settings = get_settings()

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Docstring for get_db
    
    :return: Description
    :rtype: AsyncGenerator[AsyncSession, None]
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()

