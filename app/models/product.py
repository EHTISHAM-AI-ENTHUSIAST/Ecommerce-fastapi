"""
Product Model

Defines the Product database model for e-commerce functionality.
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Product(Base):
    """
    Product model for e-commerce catalog.
    
    Attributes:
        id: Primary key
        name: Product name
        description: Detailed product description
        price: Product price (stored as float)
        category: Product category for filtering
        stock_quantity: Available inventory count
        image_url: URL to product image
        is_active: Whether product is available for sale
        owner_id: Foreign key to the user who created the product
        created_at: Product creation timestamp
        updated_at: Last update timestamp
    """
    
    __tablename__ = "products"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Product information
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    category = Column(String(100), nullable=True, index=True)
    
    # Inventory
    stock_quantity = Column(Integer, default=0)
    
    # Media
    image_url = Column(String(500), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Foreign keys
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="products")
    
    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price})>"
