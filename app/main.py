"""
E-commerce REST API - Main Application Entry Point

This is the main FastAPI application that ties everything together.
It includes all routers and configures the application settings.

Author: Ehtisham Ashraf
Email: kingehtsham0@gmail.com
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import engine, Base
from app.routers import auth, products


# Create database tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    Creates database tables when the application starts.
    """
    # Startup: Create database tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")
    yield
    # Shutdown: Clean up resources if needed
    print("👋 Application shutting down")


# Initialize FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="""
    ## E-commerce REST API
    
    A production-ready REST API for e-commerce applications.
    
    ### Features:
    - 🔐 JWT Authentication
    - 📦 Product CRUD Operations
    - 🔍 Search & Filter
    - 📄 Pagination Support
    
    ### Built by Ehtisham Ashraf
    """,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# Configure CORS middleware
# This allows frontend applications to make requests to our API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
# Each router handles a specific group of endpoints
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

app.include_router(
    products.router,
    prefix="/products",
    tags=["Products"]
)


# Root endpoint - API health check
@app.get("/", tags=["Health"])
async def root():
    """
    Root endpoint for API health check.
    Returns basic information about the API.
    """
    return {
        "message": "Welcome to E-commerce API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "status": "healthy"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring services.
    """
    return {
        "status": "healthy",
        "database": "connected"
    }
