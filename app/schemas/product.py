"""
Product Schemas

Pydantic models for product data validation and serialization.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ProductBase(BaseModel):
    """Base schema with common product fields."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    category: Optional[str] = None
    stock_quantity: int = Field(default=0, ge=0)
    image_url: Optional[str] = None


class ProductCreate(ProductBase):
    """
    Schema for creating a new product.
    
    Attributes:
        name: Product name (required)
        description: Detailed description
        price: Product price (must be > 0)
        category: Product category
        stock_quantity: Initial stock count
        image_url: URL to product image
    """
    pass


class ProductUpdate(BaseModel):
    """
    Schema for updating an existing product.
    All fields are optional - only provided fields will be updated.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = None
    stock_quantity: Optional[int] = Field(None, ge=0)
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class ProductResponse(ProductBase):
    """
    Schema for product data in API responses.
    
    Attributes:
        id: Product's unique identifier
        is_active: Whether product is available
        owner_id: ID of the user who created the product
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    id: int
    is_active: bool
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ProductList(BaseModel):
    """Schema for paginated product list response."""
    items: list[ProductResponse]
    total: int
    page: int
    pages: int
