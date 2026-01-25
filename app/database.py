"""
Database Configuration

Sets up SQLAlchemy engine, session, and base model.
Provides dependency injection for database sessions.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.config import settings


# Create SQLAlchemy engine
# For SQLite, we need connect_args to allow multi-threading
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False}  # SQLite specific
    )
else:
    # PostgreSQL or other databases
    engine = create_engine(settings.DATABASE_URL)


# Create SessionLocal class
# Each instance of SessionLocal will be a database session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Create Base class for declarative models
# All our models will inherit from this
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session.
    
    Yields a database session and ensures it's closed after use.
    Use this with FastAPI's Depends() for dependency injection.
    
    Example:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
