#!/usr/bin/python3
"""Configuration test - Compatible with pytest-asyncio < 0.24.0"""

import sys
import os
import asyncio
from typing import AsyncGenerator, Generator
from httpx import ASGITransport, AsyncClient
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ["SUPPRESS_SEND"] = "1"

from app.main import app
from app.db.session import get_db
from app.db.base_model import Base

DATABASE_URI = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(
    DATABASE_URI, connect_args={"check_same_thread": False}, poolclass=StaticPool
)

SessionLocal = async_sessionmaker(
    bind=engine_test,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create a session-wide event loop for all async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def init_test_db(event_loop):
    """Create tables once per test session."""
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a clean session and rollback after each test."""
    async with SessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Override get_db dependency and provide an AsyncClient."""

    def _get_test_db():
        yield db_session

    app.dependency_overrides[get_db] = _get_test_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
