#!/usr/bin/python3
"""
Custom Application Exceptions
"""

class BaseAuthException(Exception):
    """Base exception for auth errors"""
    pass

class UserAlreadyExistsError(BaseAuthException):
    """Raised when registering an existing user"""
    def __init__(self, message="User already exists"):
        self.message = message
        super().__init__(self.message)

class RegistrationError(BaseAuthException):
    """Raised when registration fails deeply"""
    def __init__(self, message="Registration failed"):
        self.message = message
        super().__init__(self.message)

class InvalidTokenError(BaseAuthException):
    """Raised when token is invalid or expired"""
    def __init__(self, message="Invalid or expired token"):
        self.message = message
        super().__init__(self.message)

class UserNotFoundError(BaseAuthException):
    """Raised when user is not found"""
    def __init__(self, message="User not found"):
        self.message = message
        super().__init__(self.message)

class AuthenticationError(BaseAuthException):
    """Raised when authentication fails"""
    def __init__(self, message="Incorrect email or password"):
        self.message = message
        super().__init__(self.message)
