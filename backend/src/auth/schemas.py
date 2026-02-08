from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr
    username: str


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str

    @validator('password')
    def validate_password(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')

        has_digit = any(c.isdigit() for c in v)
        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_symbol = any(not c.isalnum() for c in v)

        if not (has_digit and has_upper and has_lower and has_symbol):
            raise ValueError(
                'Password must contain at least one uppercase letter, '
                'one lowercase letter, one digit, and one symbol'
            )

        return v


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str
    password: str


class UserResponse(UserBase):
    """Schema for returning user information."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token data."""
    username: Optional[str] = None


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None

    @validator('password', pre=True)
    def validate_password_optional(cls, v):
        """Validate password if provided."""
        if v is None:
            return v

        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')

        has_digit = any(c.isdigit() for c in v)
        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_symbol = any(not c.isalnum() for c in v)

        if not (has_digit and has_upper and has_lower and has_symbol):
            raise ValueError(
                'Password must contain at least one uppercase letter, '
                'one lowercase letter, one digit, and one symbol'
            )

        return v


class ChangePasswordRequest(BaseModel):
    """Schema for changing user password."""
    current_password: str
    new_password: str

    @validator('new_password')
    def validate_new_password(cls, v):
        """Validate new password strength."""
        if len(v) < 8:
            raise ValueError('New password must be at least 8 characters long')

        has_digit = any(c.isdigit() for c in v)
        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_symbol = any(not c.isalnum() for c in v)

        if not (has_digit and has_upper and has_lower and has_symbol):
            raise ValueError(
                'New password must contain at least one uppercase letter, '
                'one lowercase letter, one digit, and one symbol'
            )

        return v


class PasswordResetRequest(BaseModel):
    """Schema for requesting password reset."""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Schema for confirming password reset."""
    token: str
    new_password: str

    @validator('new_password')
    def validate_new_password(cls, v):
        """Validate new password strength."""
        if len(v) < 8:
            raise ValueError('New password must be at least 8 characters long')

        has_digit = any(c.isdigit() for c in v)
        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_symbol = any(not c.isalnum() for c in v)

        if not (has_digit and has_upper and has_lower and has_symbol):
            raise ValueError(
                'New password must contain at least one uppercase letter, '
                'one lowercase letter, one digit, and one symbol'
            )

        return v