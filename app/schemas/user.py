"""
User Schemas

Pydantic models for user data validation and serialization.
These schemas define the shape of data for API requests and responses.
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """Base schema with common user fields."""
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """
    Schema for user registration.
    
    Attributes:
        email: Valid email address
        password: Plain text password (will be hashed)
        full_name: Optional display name
    """
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")


class UserLogin(BaseModel):
    """
    Schema for user login.
    
    Attributes:
        email: User's email address
        password: User's password
    """
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """
    Schema for user data in API responses.
    Excludes sensitive data like password.
    
    Attributes:
        id: User's unique identifier
        email: User's email
        full_name: User's display name
        is_active: Account status
        created_at: Registration timestamp
    """
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        # Allow ORM model to Pydantic conversion
        from_attributes = True


class Token(BaseModel):
    """
    Schema for JWT token response.
    
    Attributes:
        access_token: The JWT token string
        token_type: Type of token (always "bearer")
    """
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """
    Schema for decoded token data.
    
    Attributes:
        email: Email extracted from token
    """
    email: Optional[str] = None
