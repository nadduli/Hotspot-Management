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
    result = await db.execute(select(Role.name).where(Role.name.in_(ROLES)))
    existing_roles = set(result.scalars().all())

    for role_name in ROLES:
        if role_name not in existing_roles:
            logger.info(f"Creating role: {role_name}")
            new_role = Role(name=role_name)
            db.add(new_role)
    
    await db.commit()