"""
Products Router

Handles all product CRUD operations and search functionality.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models.product import Product
from app.models.user import User
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, ProductList
from app.utils.security import get_current_user


router = APIRouter()


@router.get("/", response_model=list[ProductResponse])
async def get_products(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to return"),
    category: Optional[str] = Query(None, description="Filter by category"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    db: Session = Depends(get_db)
):
    """
    Get a list of all active products with optional filtering.
    
    - **skip**: Number of items to skip for pagination
    - **limit**: Maximum number of items to return (max 100)
    - **category**: Filter products by category
    - **min_price**: Filter products with price >= min_price
    - **max_price**: Filter products with price <= max_price
    """
    # Start with base query for active products
    query = db.query(Product).filter(Product.is_active == True)
    
    # Apply filters if provided
    if category:
        query = query.filter(Product.category == category)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    
    # Apply pagination and return results
    products = query.offset(skip).limit(limit).all()
    return products


@router.get("/search", response_model=list[ProductResponse])
async def search_products(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(10, ge=1, le=50, description="Number of results"),
    db: Session = Depends(get_db)
):
    """
    Search products by name or description.
    
    - **q**: Search query string (searches in name and description)
    - **limit**: Maximum number of results to return
    """
    # Search in name and description using LIKE
    search_term = f"%{q}%"
    products = db.query(Product).filter(
        Product.is_active == True,
        or_(
            Product.name.ilike(search_term),
            Product.description.ilike(search_term)
        )
    ).limit(limit).all()
    
    return products


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Get a single product by its ID.
    
    - **product_id**: The unique identifier of the product
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )
    
    return product


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new product.
    
    Requires authentication. The authenticated user becomes the product owner.
    
    - **name**: Product name (required)
    - **description**: Product description
    - **price**: Product price (must be > 0)
    - **category**: Product category
    - **stock_quantity**: Initial stock quantity
    - **image_url**: URL to product image
    """
    # Create new product with owner set to current user
    new_product = Product(
        **product_data.model_dump(),
        owner_id=current_user.id
    )
    
    # Save to database
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return new_product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an existing product.
    
    Requires authentication. Only the product owner or admin can update.
    Only provided fields will be updated.
    """
    # Find the product
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )
    
    # Check ownership (owner or admin can update)
    if product.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this product"
        )
    
    # Update only provided fields
    update_data = product_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    # Save changes
    db.commit()
    db.refresh(product)
    
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a product.
    
    Requires authentication. Only the product owner or admin can delete.
    This performs a soft delete (sets is_active to False).
    """
    # Find the product
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )
    
    # Check ownership
    if product.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this product"
        )
    
    # Soft delete - just mark as inactive
    product.is_active = False
    db.commit()
    
    return None


@router.get("/categories/list", response_model=list[str])
async def get_categories(db: Session = Depends(get_db)):
    """
    Get a list of all unique product categories.
    """
    categories = db.query(Product.category).filter(
        Product.is_active == True,
        Product.category != None
    ).distinct().all()
    
    return [cat[0] for cat in categories if cat[0]]
