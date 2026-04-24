"""
Nutrition Engine - Calculate and score nutrition content.
Provides health metrics for cart intelligence and health-first persona.
"""

from typing import Dict, List


class NutritionEngine:
    """Calculate nutrition profiles and provide health scoring."""

    # Mock nutrition data (in production, fetch from item database)
    NUTRITION_DATA = {
        "chicken_biryani": {"calories": 450, "protein": 25, "carbs": 55, "fat": 12},
        "paneer_butter_masala": {"calories": 380, "protein": 20, "carbs": 30, "fat": 18},
        "dal_makhani": {"calories": 220, "protein": 12, "carbs": 25, "fat": 8},
        "tandoori_chicken": {"calories": 165, "protein": 28, "carbs": 0, "fat": 6},
        "vegetable_fried_rice": {"calories": 280, "protein": 8, "carbs": 40, "fat": 10},
        "grilled_fish": {"calories": 200, "protein": 35, "carbs": 0, "fat": 7},
        "margherita_pizza": {"calories": 285, "protein": 12, "carbs": 35, "fat": 10},
        "greek_salad": {"calories": 150, "protein": 8, "carbs": 12, "fat": 8},
        "garlic_naan": {"calories": 310, "protein": 8, "carbs": 50, "fat": 8},
        "ice_cream": {"calories": 200, "protein": 4, "carbs": 25, "fat": 11},
    }

    def get_item_nutrition(self, item_id: str) -> Dict:
        """Get nutrition info for an item."""
        return self.NUTRITION_DATA.get(
            item_id.lower().replace(" ", "_"),
            {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
        )

    def calculate_cart_nutrition(self, items: List[Dict]) -> Dict:
        """
        Calculate total nutrition for cart.
        Items: [{item_id, quantity}, ...]
        """
        total = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}

        for item in items:
            nutrition = self.get_item_nutrition(item["item_id"])
            qty = item.get("quantity", 1)
            
            total["calories"] += nutrition["calories"] * qty
            total["protein"] += nutrition["protein"] * qty
            total["carbs"] += nutrition["carbs"] * qty
            total["fat"] += nutrition["fat"] * qty

        return total

    def health_score(self, nutrition: Dict) -> float:
        """
        Calculate health score (0-10) based on nutrition.
        Favors: high protein, moderate calories, low fat.
        """
        score = 0.0
        
        # Protein score (higher is better, 25g = max points)
        protein_score = min(10, nutrition["protein"] / 25 * 10)
        score += protein_score * 0.4

        # Calorie score (200-600 is ideal)
        cal = nutrition["calories"]
        if 200 <= cal <= 600:
            calorie_score = 10
        elif cal < 200:
            calorie_score = cal / 200 * 10
        else:
            calorie_score = max(0, 10 - (cal - 600) / 400)
        score += calorie_score * 0.4

        # Fat score (lower is better, 15g = max)
        fat_score = max(0, 10 - nutrition["fat"] / 15 * 10)
        score += fat_score * 0.2

        return round(score, 1)

    def detect_nutrition_gaps(self, current_nutrition: Dict) -> List[str]:
        """
        Detect nutrition gaps in current selection.
        Returns suggestions for improvement.
        """
        gaps = []

        if current_nutrition["protein"] < 20:
            gaps.append("Add high-protein item")
        
        if current_nutrition["calories"] < 300:
            gaps.append("Add more calories")
        
        if current_nutrition["fat"] > 50:
            gaps.append("Consider lower-fat option")

        if current_nutrition["carbs"] < 40:
            gaps.append("Add carbs for energy")

        return gaps

    def suggest_addons(
        self,
        current_nutrition: Dict,
        available_items: List[Dict],
        user_goal: str = "balanced"
    ) -> List[str]:
        """
        Suggest add-on items based on nutrition goals.
        user_goal: health-first, balanced, indulgent
        """
        suggestions = []

        if user_goal == "health-first":
            # Suggest high-protein, low-cal items
            for item in available_items:
                nutrition = self.get_item_nutrition(item["id"])
                if nutrition["protein"] > 20 and nutrition["calories"] < 250:
                    suggestions.append(item["name"])
        
        elif user_goal == "indulgent":
            # Suggest tasty, satisfying items
            suggestions = [item["name"] for item in available_items[:3]]

        return suggestions[:3]  # Top 3 suggestions

    def macro_ratios(self, nutrition: Dict) -> Dict:
        """Calculate macro ratios (protein:carbs:fat)."""
        total = nutrition["protein"] + nutrition["carbs"] + nutrition["fat"]
        
        if total == 0:
            return {"protein": 0, "carbs": 0, "fat": 0}

        return {
            "protein": round(nutrition["protein"] / total * 100),
            "carbs": round(nutrition["carbs"] / total * 100),
            "fat": round(nutrition["fat"] / total * 100)
        }
