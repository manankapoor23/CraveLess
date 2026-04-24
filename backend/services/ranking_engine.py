"""
Ranking Engine - Multi-objective optimization for recommendations.
Scores items using preference match, price, delivery time, health score, and novelty.
"""

from typing import List, Dict
import math


class RankingEngine:
    """
    Multi-objective scoring and ranking.
    Combines multiple criteria with adjustable weights per persona.
    """

    PERSONA_WEIGHTS = {
        "health-first": {
            "preference_match": 0.25,
            "health_score": 0.40,
            "price": 0.15,
            "delivery_time": 0.10,
            "novelty": 0.10
        },
        "budget": {
            "preference_match": 0.30,
            "health_score": 0.10,
            "price": 0.45,
            "delivery_time": 0.10,
            "novelty": 0.05
        },
        "fast_delivery": {
            "preference_match": 0.30,
            "health_score": 0.10,
            "price": 0.15,
            "delivery_time": 0.40,
            "novelty": 0.05
        },
        "explore": {
            "preference_match": 0.20,
            "health_score": 0.15,
            "price": 0.20,
            "delivery_time": 0.15,
            "novelty": 0.30  # Favor new items
        },
        "balanced": {
            "preference_match": 0.30,
            "health_score": 0.20,
            "price": 0.20,
            "delivery_time": 0.15,
            "novelty": 0.15
        }
    }

    def score_item(
        self,
        item: Dict,
        user_preferences: Dict = None,
        persona: str = "balanced",
        user_goal: str = "balanced"
    ) -> Dict:
        """
        Score a single item across multiple objectives.
        Returns: {item, score, components}
        """
        weights = self.PERSONA_WEIGHTS.get(persona, self.PERSONA_WEIGHTS["balanced"])

        # Calculate individual scores (0-10 scale)
        pref_score = self._preference_score(item, user_preferences)
        health_score = self._health_score(item)
        price_score = self._price_score(item)
        delivery_score = self._delivery_score(item)
        novelty_score = self._novelty_score(item)

        # Weighted sum
        final_score = (
            pref_score * weights["preference_match"] +
            health_score * weights["health_score"] +
            price_score * weights["price"] +
            delivery_score * weights["delivery_time"] +
            novelty_score * weights["novelty"]
        )

        return {
            "item": item,
            "final_score": round(final_score, 2),
            "components": {
                "preference_match": round(pref_score, 1),
                "health_score": round(health_score, 1),
                "price": round(price_score, 1),
                "delivery_time": round(delivery_score, 1),
                "novelty": round(novelty_score, 1)
            }
        }

    def rank_items(
        self,
        items: List[Dict],
        user_preferences: Dict = None,
        persona: str = "balanced",
        limit: int = None
    ) -> List[Dict]:
        """
        Rank items and optionally return top-N.
        """
        scored = [self.score_item(item, user_preferences, persona) for item in items]
        ranked = sorted(scored, key=lambda x: x["final_score"], reverse=True)
        
        if limit:
            ranked = ranked[:limit]

        return ranked

    def _preference_score(self, item: Dict, preferences: Dict = None) -> float:
        """Score based on user preference history."""
        if not preferences:
            return 5.0  # Neutral

        item_id = item.get("id")
        if item_id in preferences:
            pref = preferences[item_id]
            rating = pref.get("rating", 3.0)
            # Scale 1-5 rating to 0-10 score
            return (rating - 1) / 4 * 10
        
        return 5.0

    def _health_score(self, item: Dict) -> float:
        """
        Score based on health metrics (0-10).
        Mock: use item.health_score or calculate.
        """
        return item.get("health_score", 5.0)

    def _price_score(self, item: Dict) -> float:
        """Score based on value (0-10). Lower price = higher score."""
        price = item.get("price", 200)
        
        # Scoring: <100=10, 100-300=linear decay, >500=0
        if price < 100:
            return 10.0
        elif price <= 500:
            return max(0, 10 - (price - 100) / 40)
        else:
            return 0.0

    def _delivery_score(self, item: Dict) -> float:
        """Score based on delivery time (0-10). Lower time = higher score."""
        delivery_mins = item.get("delivery_time_mins", 30)
        
        # Scoring: <15min=10, 15-60min=decay, >60min=low
        if delivery_mins <= 15:
            return 10.0
        elif delivery_mins <= 60:
            return max(2, 10 - (delivery_mins - 15) / 6)
        else:
            return 2.0

    def _novelty_score(self, item: Dict) -> float:
        """
        Score based on novelty (0-10).
        New items = high, frequently seen = low.
        """
        is_new = item.get("is_new", False)
        times_seen = item.get("times_seen_by_user", 0)
        
        if is_new:
            return 9.0
        elif times_seen == 0:
            return 8.0
        elif times_seen < 3:
            return 6.0
        else:
            return min(3.0, 10 - times_seen)

    def get_top_3_with_explanation(
        self,
        items: List[Dict],
        user_preferences: Dict = None,
        persona: str = "balanced"
    ) -> List[Dict]:
        """
        Get top-3 recommendations with human-readable explanations.
        """
        ranked = self.rank_items(items, user_preferences, persona, limit=3)
        
        explanations = []
        for idx, result in enumerate(ranked, 1):
            components = result["components"]
            item = result["item"]
            
            # Build explanation
            reasons = []
            if components["preference_match"] > 7:
                reasons.append("you loved it before")
            if components["health_score"] > 7:
                reasons.append("healthy choice")
            if components["price"] > 8:
                reasons.append("great value")
            if components["delivery_time"] > 8:
                reasons.append("quick delivery")
            if components["novelty"] > 7:
                reasons.append("something new")

            explanations.append({
                "rank": idx,
                "item": item,
                "score": result["final_score"],
                "explanation": ", ".join(reasons) if reasons else "great overall option"
            })

        return explanations
