"""User model with OAuth integration."""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
from db.database import Base


class User(Base):
    """User entity with OAuth credentials and preferences."""
    __tablename__ = "users"

    id = Column(String, primary_key=True)  # OAuth provider user ID
    email = Column(String, unique=True, index=True)
    name = Column(String)
    provider = Column(String)  # "google", "swiggy", etc.
    oauth_token = Column(String)  # Refresh token stored securely
    oauth_token_expiry = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Profile data
    dietary_restrictions = Column(JSON, default=list)  # ["vegetarian", "gluten-free"]
    health_score_preference = Column(String, default="balanced")  # health-first, balanced, none
    budget_preference = Column(String, default="medium")  # cheap, medium, premium
    
    preferences = relationship("Preference", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.email}>"
