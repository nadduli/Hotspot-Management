#!/usr/bin/python3
"""
Authentication Service
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.models.roles import Role
from app.schemas.auth import UserCreate
from app.core.security import verify_password, hash_password
from app.core.config import get_settings
import uuid

settings = get_settings()


class AuthService:
    """
    Service for handling authentication logic
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def authenticate_user(self, email: str, password: str) -> User | None:
        """
        Authenticate a user by email and password
        """
        result = await self.db.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    async def create_user(self, user_in: UserCreate, organization_id: uuid.UUID, role_name: str = "ADMIN") -> User:
        """
        Create a new user with a specific role
        """
        hashed_password = hash_password(user_in.password)
        
        # Fetch role
        result = await self.db.execute(select(Role).where(Role.name == role_name))
        role = result.scalars().first()
        if not role:
            # Fallback or error? For now, let's assume roles exist via init_db
            # But strictly we should handle this.
            raise ValueError(f"Role {role_name} not found")

        db_user = User(
            name=user_in.name,
            email=user_in.email,
            password=hashed_password,
            phone=user_in.phone,
            organization_id=organization_id,
        )
        db_user.roles.append(role)
        
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user
