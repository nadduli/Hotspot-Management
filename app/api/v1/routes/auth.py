from fastapi import APIRouter, Depends, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from app.db.session import get_db
from app.services.auth_service import AuthService
from app.services.token_service import create_verification_token, create_access_token
from app.services.email_service import EmailService
from app.utils.logger import logger
from app.core.exceptions import (
    UserAlreadyExistsError,
    RegistrationError,
    InvalidTokenError,
    UserNotFoundError,
    AuthenticationError
)
from app.schemas.user import UserRegistrationRequest, UserRegistrationResponse, UserLoginRequest
from app.schemas.token import Token
from app.api.deps import get_current_user, get_current_active_user, get_current_user_with_role
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.responses import fail_response, success_response



router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get(
    "/me",
    summary="Get Current User",
    response_description="Current user profile",
)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user"""
    user_response = UserRegistrationResponse(
        id=str(current_user.id),
        full_name=current_user.full_name,
        email=current_user.email,
        email_verified=current_user.email_verified,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
    )
    return success_response(
        status_code=status.HTTP_200_OK,
        message="User profile retrieved",
        data=user_response.model_dump(),
    )


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
async def register(
    user_data: UserRegistrationRequest, 
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """register new user"""
    logger.info("Registration attempt for email: %s", user_data.email)
    try:
        user = await AuthService.register_user(db, user_data)
        
        # Schedule email verification
        try:
            token = create_verification_token(user.email)
            background_tasks.add_task(EmailService.send_verification_email, user, token)
        except Exception as e:
            logger.error(f"Failed to schedule verification email: {e}")

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
            message="Welcome to Hotspot! Your account has been created successfully.",
            data=user_response.model_dump(),
        )

    except UserAlreadyExistsError as e:
        return fail_response(status_code=status.HTTP_409_CONFLICT, message=str(e))
    except RegistrationError as e:
        return fail_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in register: {e}")
        return fail_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            message="An unexpected error occurred"
        )


@router.get(
    "/verify-email",
    status_code=status.HTTP_200_OK,
    summary="Verify User Email",
    response_description="Verification status",
    responses={
        200: {"description": "Email verified successfully"},
        400: {"description": "Invalid or expired token"},
        404: {"description": "User not found"},
    }
)
async def verify_email(token: str, db: AsyncSession = Depends(get_db)):
    """Verify user email"""
    try:
        await AuthService.verify_email(db, token)
        return success_response(
            status_code=status.HTTP_200_OK,
            message="Email verified successfully",
            data=None,
        )
    except UserNotFoundError as e:
        return fail_response(status_code=status.HTTP_404_NOT_FOUND, message=str(e))
    except InvalidTokenError as e:
        return fail_response(status_code=status.HTTP_400_BAD_REQUEST, message=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in verify_email: {e}")
        return fail_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            message="An unexpected error occurred"
        )


@router.post(
    "/token",
    response_model=Token,
    summary="OAuth2 Compatible Login",
    description="Login using form data (username/password). Used by Swagger UI."
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """OAuth2 compatible token login"""
    try:
        user = await AuthService.authenticate_user(db, form_data.username, form_data.password)
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    except AuthenticationError as e:
        # OAuth2 requires 400 Bad Request for invalid credentials usually, or 401
        # FastAPI security expects specific exception for headers usually, but returning dict works if model matches.
        # However, for OAuth2 compliance, we strictly often raise HTTPException.
        # But we are using our fail_response wrapper usually? 
        # Wait, for this specific endpoint, we should return the Token model directly, not wrapped in success_response structure
        # because Swagger UI expects exact JSON matching the Security Scheme.
        return fail_response(status_code=status.HTTP_401_UNAUTHORIZED, message=str(e))
    except Exception as e:
        logger.error(f"Login error: {e}")
        return fail_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Login failed")


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="User Login",
    response_description="Login response with token",
)
async def login(
    login_data: UserLoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """JSON Login"""
    try:
        user = await AuthService.authenticate_user(db, login_data.email, login_data.password)
        access_token = create_access_token(data={"sub": user.email})
        
        token_data = {"access_token": access_token, "token_type": "bearer"}
        
        return success_response(
            status_code=status.HTTP_200_OK,
            message="Login successful",
            data=token_data
        )
    except AuthenticationError as e:
        return fail_response(status_code=status.HTTP_401_UNAUTHORIZED, message=str(e))
    except Exception as e:
        logger.error(f"Login error: {e}")
        return fail_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Login failed")
