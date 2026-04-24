"""Preference and memory models for taste graph."""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from db.database import Base


class Preference(Base):
    """User preferences and taste profile."""
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    
    # Ingredient/cuisine preferences
    item_id = Column(String)  # Reference to menu item
    item_name = Column(String)
    category = Column(String)  # cuisine, ingredient, brand
    
    # Preference signal
    rating = Column(Float)  # 1-5 scale
    preferred = Column(String, default="neutral")  # liked, disliked, neutral, never_again
    
    # Context
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    count = Column(Integer, default=1)  # How many times selected/rated
    
    user = relationship("User", back_populates="preferences")
    
    def __repr__(self):
        return f"<Preference {self.item_name} -> {self.preferred}>"


class Order(Base):
    """Past orders for memory and recall."""
    __tablename__ = "orders"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    
    items = Column(JSON)  # [{item_id, name, price, quantity}]
    total_price = Column(Float)
    nutrition_summary = Column(JSON)  # {calories, protein, carbs, fat}
    
    created_at = Column(DateTime, default=datetime.utcnow)
    rating = Column(Float)  # User rating of order (1-5)
    feedback = Column(String)  # Why they liked/disliked it
    
    user = relationship("User", back_populates="orders")
    
    def __repr__(self):
        return f"<Order {self.id} by {self.user_id}>"


class TasteGraphNode(Base):
    """Taste graph nodes: ingredients, cuisines, attributes."""
    __tablename__ = "taste_graph_nodes"

    id = Column(String, primary_key=True)
    type = Column(String)  # ingredient, cuisine, attribute, brand
    name = Column(String, unique=True, index=True)
    
    # Node properties
    properties = Column(JSON)  # {color, healthScore, price_tier, etc.}
    
    created_at = Column(DateTime, default=datetime.utcnow)


class TasteGraphEdge(Base):
    """Relationships in taste graph."""
    __tablename__ = "taste_graph_edges"

    id = Column(Integer, primary_key=True)
    from_node_id = Column(String, ForeignKey("taste_graph_nodes.id"))
    to_node_id = Column(String, ForeignKey("taste_graph_nodes.id"))
    
    relationship_type = Column(String)  # pairs_with, complements, contradicts, alternative
    strength = Column(Float, default=1.0)  # Weight of relationship
    
    created_at = Column(DateTime, default=datetime.utcnow)
