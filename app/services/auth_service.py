from typing import Optional, Tuple
from fastapi import HTTPException, status
from app.models.user import User
from app.core.security import hash_password, verify_password
from app.core.exceptions import (
    UserAlreadyExistsError,
    RegistrationError,
    InvalidTokenError,
    UserNotFoundError,
    AuthenticationError
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserRegistrationRequest
from sqlalchemy.exc import IntegrityError
from app.utils.logger import logger
from .token_service import create_verification_token, verify_registration_token
from .email_service import EmailService


class AuthService:
    @staticmethod
    async def register_user(
        db: AsyncSession, user_data: UserRegistrationRequest
    ) -> User:
        """
        Create a new user account.
        
        Returns:
            User: The created user instance.
            
        Raises:
            UserAlreadyExistsError: If email is already registered.
            RegistrationError: For other registration failures.
        """
        try:
            existing_user = await User.fetch_unique(db, email=user_data.email.lower())
            if existing_user is not None:
                raise UserAlreadyExistsError("Email already registered")

            new_user = User(
                full_name=user_data.full_name,
                email=user_data.email.lower(),
                email_verified=False,
                password_hash=hash_password(user_data.password),
            )

            new_user.add(db)
            await db.flush()
            await db.commit()
            await db.refresh(new_user)

            return new_user

        except UserAlreadyExistsError as e:
            # Re-raise known business exceptions
            raise e
        except IntegrityError:
            await db.rollback()
            logger.error(
                "Database integrity error during registration for email: %s",
                user_data.email,
            )
            raise UserAlreadyExistsError("User already exists")
        except Exception as e:
            await db.rollback()
            logger.error(
                "Error creating user %s: %s",
                user_data.email,
                str(e),
                exc_info=True,
            )
            raise RegistrationError("An error occurred while creating the account")

    @staticmethod
    async def verify_email(db: AsyncSession, token: str) -> bool:
        """
        Verify user email.
        
        Returns:
            bool: True if verification successful (or already verified).
            
        Raises:
            InvalidTokenError: If token is invalid/expired.
            UserNotFoundError: If user from token doesn't exist.
        """
        try:
            email = verify_registration_token(token)
            user = await User.fetch_unique(db, email=email)
            
            if not user:
                raise UserNotFoundError("User not found")
                
            if user.email_verified:
                return True
                
            user.email_verified = True
            await user.update(db)
            return True
            
        except InvalidTokenError:
            raise
        except UserNotFoundError:
            raise
        except Exception as e:
            # Map other exceptions (like itsdangerous errors) to InvalidTokenError
            logger.error(f"Verification error: {e}")
            raise InvalidTokenError("Invalid or expired token")

    @staticmethod
    async def authenticate_user(db: AsyncSession, email: str, password: str) -> User:
        """
        Authenticate user by email and password.
        
        Returns:
            User: The authenticated user.
            
        Raises:
            AuthenticationError: If credentials are invalid.
        """
        try:
            user = await User.fetch_unique(db, email=email.lower())
            if not user:
                raise AuthenticationError("Incorrect email or password")
                
            if not verify_password(password, user.password_hash):
                raise AuthenticationError("Incorrect email or password")
                
            return user
        except AuthenticationError:
            raise
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            raise AuthenticationError("Authentication failed")
