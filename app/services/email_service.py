#!/usr/bin/python3
"""Email Service Module"""

from fastapi_mail import FastMail, MessageSchema, MessageType
from app.core.config import get_settings
from app.core.mail_config import mail_conf
from app.models.user import User

settings = get_settings()


class EmailService:
    @staticmethod
    async def send_verification_email(user: User, token: str):
        """Send verification email to user"""
        
        verification_url = f"{settings.BASE_URI}/api/v1/auth/verify-email?token={token}"
        
        message = MessageSchema(
            subject="Confirm your Hotspot Management Account",
            recipients=[user.email],
            template_body={"url": verification_url, "name": user.full_name},
            subtype=MessageType.html,
        )
        
        fm = FastMail(mail_conf)
        await fm.send_message(message, template_name="verification.html")
