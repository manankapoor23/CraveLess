"""
Database configuration and session management.
Supports PostgreSQL and SQLite fallback.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL from environment, defaults to SQLite for quick start
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./craveless.db"
)

# Use check_same_thread=False for SQLite only
if "sqlite" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency for FastAPI to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize all tables."""
    Base.metadata.create_all(bind=engine)
