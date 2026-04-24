"""
Recommendations routes - Get personalized top-3 recommendations.
Integrates all services: ranking, taste graph, memory, nutrition.
"""

from fastapi import APIRouter, HTTPException, Cookie, Query
from pydantic import BaseModel
from typing import List, Optional
from services.ranking_engine import RankingEngine
from services.taste_graph import TasteGraph
from services.memory_engine import MemoryEngine
from services.nutrition_engine import NutritionEngine
from data.mock_menu import MOCK_MENU

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

# Initialize engines (in production: use dependency injection)
ranking_engine = RankingEngine()
taste_graph = TasteGraph()
memory_engine = MemoryEngine()
nutrition_engine = NutritionEngine()


class RecommendationRequest(BaseModel):
    """Recommendation request with intent and persona."""
    intent: Optional[str] = None  # "cheap", "high protein", "fast", "new", etc.
    persona: str = "balanced"  # health-first, budget, fast_delivery, explore, balanced
    filters: Optional[dict] = None  # {min_price, max_price, max_delivery_mins, etc.}


class RecommendedItem(BaseModel):
    """Single recommendation with explanation."""
    rank: int
    item: dict
    score: float
    explanation: str
    memory_signal: Optional[dict] = None  # "you loved this before"
    nutrition: Optional[dict] = None


class RecommendationResponse(BaseModel):
    """Top-3 recommendations response."""
    recommendations: List[RecommendedItem]
    summary: dict  # {user_intent, persona, reasoning}


def _get_or_create_user_session(session_token: Optional[str] = None) -> str:
    """
    Get user ID from session or create mock user.
    In production: verify JWT or session token.
    """
    if session_token:
        # In production: lookup user from session
        return session_token[:8]  # Mock: use first 8 chars
    
    return "anonymous"


@router.post("/get-top-3", response_model=RecommendationResponse)
async def get_recommendations(
    request: RecommendationRequest,
    session_token: Optional[str] = Cookie(None)
):
    """
    Get top-3 personalized recommendations.
    
    CORE ENDPOINT: Integrates all decision-making logic.
    """
    user_id = _get_or_create_user_session(session_token)
    
    # Apply filters
    filtered_menu = MOCK_MENU.copy()
    
    if request.filters:
        if "max_price" in request.filters:
            filtered_menu = [
                item for item in filtered_menu
                if item["price"] <= request.filters["max_price"]
            ]
        
        if "max_delivery_mins" in request.filters:
            filtered_menu = [
                item for item in filtered_menu
                if item["delivery_time_mins"] <= request.filters["max_delivery_mins"]
            ]
        
        if "dietary_restrictions" in request.filters:
            restrictions = request.filters["dietary_restrictions"]
            filtered_menu = [
                item for item in filtered_menu
                if not any(r in item.get("allergens", []) for r in restrictions)
            ]

    if not filtered_menu:
        raise HTTPException(status_code=400, detail="No items match your filters")

    # Get user preferences
    user_preferences = memory_engine.get_user_preferences(user_id)

    # Get top-3 using ranking engine
    ranked = ranking_engine.get_top_3_with_explanation(
        filtered_menu,
        user_preferences=user_preferences,
        persona=request.persona
    )

    # Enrich with nutrition and memory signals
    recommendations = []
    for result in ranked:
        item = result["item"]
        nutrition = nutrition_engine.get_item_nutrition(item["id"])
        memory_signal = memory_engine.get_memory_signal(user_id, item["id"])

        recommendations.append(
            RecommendedItem(
                rank=result["rank"],
                item=item,
                score=result["score"],
                explanation=result["explanation"],
                memory_signal=memory_signal,
                nutrition=nutrition
            )
        )

    # Build reasoning summary
    reasoning = {
        "intent": request.intent or "balanced",
        "persona": request.persona,
        "filters_applied": request.filters or {},
        "total_items_considered": len(filtered_menu),
        "decision_logic": "multi-objective optimization across preference, health, price, delivery, novelty"
    }

    return RecommendationResponse(
        recommendations=recommendations,
        summary=reasoning
    )


@router.post("/record-preference")
async def record_preference(
    item_id: str,
    rating: float,
    session_token: Optional[str] = Cookie(None)
):
    """
    Record user preference/rating for an item.
    Feeds into memory engine and taste graph.
    """
    user_id = _get_or_create_user_session(session_token)
    
    if not (0.0 <= rating <= 5.0):
        raise HTTPException(status_code=400, detail="Rating must be 0-5")

    # Find item
    item = next((i for i in MOCK_MENU if i["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Record preference
    memory_engine.record_preference(
        user_id=user_id,
        item_id=item_id,
        item_name=item["name"],
        rating=rating,
        category=item["category"]
    )

    # Propagate through taste graph
    if rating >= 4.0:  # User liked it
        propagated = taste_graph.propagate_preference(item_id, rating)
        # In production: update memory for related items too
    
    return {
        "status": "success",
        "message": f"Preference recorded: {item['name']} = {rating}/5"
    }


@router.post("/never-again")
async def mark_never_again(
    item_id: str,
    session_token: Optional[str] = Cookie(None)
):
    """Mark item as 'never show again'."""
    user_id = _get_or_create_user_session(session_token)
    
    item = next((i for i in MOCK_MENU if i["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    memory_engine.mark_never_again(user_id, item_id)
    
    return {
        "status": "success",
        "message": f"'{item['name']}' will no longer be recommended"
    }


@router.get("/similar/{item_id}")
async def get_similar_items(item_id: str, limit: int = Query(5)):
    """Get similar items based on taste graph."""
    similar_nodes = taste_graph.find_alternatives(item_id, limit=limit)
    
    # Map nodes back to menu items
    similar_items = []
    for node_id, strength in similar_nodes:
        item = next((i for i in MOCK_MENU if i["id"] == node_id), None)
        if item:
            similar_items.append({
                "item": item,
                "similarity_score": round(strength, 2)
            })

    return {
        "original_item_id": item_id,
        "similar_items": similar_items
    }


@router.get("/persona-comparison")
async def compare_personas(session_token: Optional[str] = Cookie(None)):
    """
    Compare top-3 across all personas.
    Useful for UX: show how rankings change by persona.
    """
    user_id = _get_or_create_user_session(session_token)
    user_preferences = memory_engine.get_user_preferences(user_id)
    
    comparison = {}
    
    for persona in ["health-first", "budget", "fast_delivery", "explore", "balanced"]:
        ranked = ranking_engine.get_top_3_with_explanation(
            MOCK_MENU,
            user_preferences=user_preferences,
            persona=persona
        )
        comparison[persona] = [
            {
                "rank": r["rank"],
                "item_name": r["item"]["name"],
                "score": r["score"]
            }
            for r in ranked
        ]

    return {"persona_comparison": comparison}
