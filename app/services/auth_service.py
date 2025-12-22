#!/usr/bin/python3
"""user service module"""
from typing import Optional, Tuple
from app.models.user import User
from app.core.security import hash_password
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserRegistrationRequest
from sqlalchemy.exc import IntegrityError
from app.utils.logger import logger
from app.models.role import Role 



class AuthService:
    @staticmethod
    async def register_user(db: AsyncSession, user_data: UserRegistrationRequest) ->  Tuple[Optional[User], Optional[dict], Optional[str]]:
        """create a new user account"""
        try:
            existing_user = await User.fetch_unique(db, email=user_data.email.lower())
            context = {}
            if existing_user is not None:
                context["is_registered"] = True
                context["is_email_verified"] = existing_user.email_verified
                return existing_user, context, None
            
            
            role = await Role.fetch_unique(db, name="AGENT")
            if not role:
                return None, None, "Default role 'AGENT' not found in database"
            
            new_user = User(
                full_name=user_data.full_name,
                email=user_data.email.lower() if user_data.email else None,
                email_verified=True,
                password_hash=hash_password(user_data.password),
                role_id=role.id,               
                branch_id=user_data.branch_id if hasattr(user_data, 'branch_id') else None,
            )

            new_user.add(db)
            await db.flush()

            await db.commit()
            await db.refresh(new_user)

            return new_user, None, None

        except IntegrityError:
            await db.rollback()
            logger.error(
                "Database integrity error during registration for email: %s",
                user_data.email
            )
            return None, {"message": "User already exists"}, None
        except Exception as e:
            await db.rollback()
            logger.error(
                "Error creating user %s: %s",
                user_data.email,
                str(e),
                exc_info=True,
            )
            return None, {"message": "An error occurred while creating the account"}, None
