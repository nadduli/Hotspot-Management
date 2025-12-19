#!/usr/bin/python3
"""
Database Initialization
"""
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.roles import Role

logger = logging.getLogger(__name__)

ROLES = ["ADMIN", "AGENT"]

async def init_db(db: AsyncSession) -> None:
    """
    Initialize database with default roles
    """
    for role_name in ROLES:
        result = await db.execute(select(Role).where(Role.name == role_name))
        role = result.scalars().first()
        if not role:
            logger.info(f"Creating role: {role_name}")
            new_role = Role(name=role_name)
            db.add(new_role)
    
    await db.commit()
