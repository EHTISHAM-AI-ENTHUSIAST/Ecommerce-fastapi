"""
User Model

Defines the User database model for authentication.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    """
    User model for authentication and authorization.
    
    Attributes:
        id: Primary key
        email: Unique email address (used for login)
        hashed_password: Bcrypt hashed password
        full_name: User's display name
        is_active: Whether the user account is active
        is_admin: Whether the user has admin privileges
        created_at: Account creation timestamp
        updated_at: Last update timestamp
    """
    
    __tablename__ = "users"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Authentication fields
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Profile fields
    full_name = Column(String(255), nullable=True)
    
    # Status flags
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    products = relationship("Product", back_populates="owner")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
