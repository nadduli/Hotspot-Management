#!/usr/bin/python3
"""Auth routes"""

from fastapi import APIRouter, Depends, status
from app.db.session import get_db
from app.services.auth_service import AuthService
from app.utils.logger import logger
from app.schemas.user import UserRegistrationRequest, UserRegistrationResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.responses import fail_response, success_response


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post(
    "/register",
status_code=status.HTTP_201_CREATED,
summary="Register New User",
response_description="User registration data",
responses={
    201: {"description": "User successfully registered"},
    422: {"description": "Invalid input or validation error"},
    409: {"description": "Email already registered"},
    500: {"description": "Internal server error"},
},
)
async def register(user_data: UserRegistrationRequest, db: AsyncSession = Depends(get_db)):
    """register new user"""
    logger.info("Registration attempt for email: %s", user_data.email)
    user, context, error = await AuthService.register_user(db, user_data)

    if error:
        return fail_response(status_code=500, message=error)
    
    if context and context.get("is_registered"):
        return fail_response(status_code=409, message="User already exists")
    
    if not user:
        logger.error(
            "User creation returned None without error for %s",
            user_data.email,
        )
        return fail_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Failed to create user",
        )
    
    user_response = UserRegistrationResponse(
        id=str(user.id),
        full_name=user.full_name,
        email=user.email,
        email_verified=user.email_verified,
        is_active=user.is_active,
        created_at=user.created_at,
    )

    logger.info("Registration successful for user: %s", user.email)
    return success_response(
        status_code=status.HTTP_201_CREATED,
        message="Welcome to Nora! Your account has been created successfully.",
        data=user_response.model_dump(),
    )