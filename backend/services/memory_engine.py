"""
Memory Engine - User preference tracking and recall.
Stores and retrieves user taste preferences for intelligent ranking.
"""

from typing import Dict, List, Optional
from datetime import datetime


class MemoryEngine:
    """
    In-memory preference cache with decay and recency bias.
    In production, this reads from database and caches.
    """

    def __init__(self):
        self.user_preferences: Dict[str, Dict] = {}
        self.user_order_history: Dict[str, List[Dict]] = {}

    def record_preference(
        self,
        user_id: str,
        item_id: str,
        item_name: str,
        rating: float,
        category: str = "item"
    ):
        """Record user's preference for an item."""
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {}

        self.user_preferences[user_id][item_id] = {
            "name": item_name,
            "rating": rating,
            "category": category,
            "timestamp": datetime.utcnow().isoformat(),
            "count": self.user_preferences[user_id].get(item_id, {}).get("count", 0) + 1
        }

    def record_order(self, user_id: str, order_data: Dict):
        """Record completed order."""
        if user_id not in self.user_order_history:
            self.user_order_history[user_id] = []
        
        order_data["timestamp"] = datetime.utcnow().isoformat()
        self.user_order_history[user_id].append(order_data)

    def get_user_preferences(self, user_id: str) -> Dict:
        """Get all recorded preferences for user."""
        return self.user_preferences.get(user_id, {})

    def get_item_preference(self, user_id: str, item_id: str) -> Optional[float]:
        """Get preference rating for specific item."""
        prefs = self.user_preferences.get(user_id, {})
        if item_id in prefs:
            return prefs[item_id]["rating"]
        return None

    def get_category_affinity(self, user_id: str, category: str) -> float:
        """
        Calculate user's affinity to a category.
        Returns average rating for items in category.
        """
        prefs = self.user_preferences.get(user_id, {})
        category_items = [
            v["rating"] for v in prefs.values()
            if v["category"] == category
        ]
        
        if not category_items:
            return 0.5  # Neutral default
        
        return sum(category_items) / len(category_items)

    def get_recent_items(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get recently ordered items."""
        orders = self.user_order_history.get(user_id, [])
        all_items = []
        
        for order in orders:
            all_items.extend(order.get("items", []))
        
        return all_items[-limit:]

    def mark_never_again(self, user_id: str, item_id: str):
        """Mark item as 'never show again'."""
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {}
        
        self.user_preferences[user_id][item_id] = {
            "rating": 0.0,
            "status": "never_again",
            "timestamp": datetime.utcnow().isoformat()
        }

    def get_memory_signal(self, user_id: str, item_id: str) -> Dict:
        """
        Generate memory signal for an item.
        Indicates if user has seen/ordered it before.
        """
        prefs = self.user_preferences.get(user_id, {})
        
        if item_id not in prefs:
            return {"seen": False, "signal": None}
        
        pref = prefs[item_id]
        rating = pref.get("rating", 0)
        count = pref.get("count", 1)

        signal = "liked" if rating >= 4.0 else "disliked" if rating <= 2.0 else "neutral"
        
        return {
            "seen": True,
            "signal": signal,
            "rating": rating,
            "count": count
        }

    def clear_user_memory(self, user_id: str):
        """Clear all preferences for a user (e.g., on request)."""
        if user_id in self.user_preferences:
            del self.user_preferences[user_id]
        if user_id in self.user_order_history:
            del self.user_order_history[user_id]
