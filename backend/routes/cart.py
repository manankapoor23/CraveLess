"""
Cart routes - Cart intelligence, nutrition summary, add-on suggestions.
"""

from fastapi import APIRouter, HTTPException, Cookie
from pydantic import BaseModel
from typing import List, Optional
from services.nutrition_engine import NutritionEngine
from services.ranking_engine import RankingEngine
from data.mock_menu import MOCK_MENU

router = APIRouter(prefix="/cart", tags=["cart"])

# Initialize engines
nutrition_engine = NutritionEngine()
ranking_engine = RankingEngine()


class CartItem(BaseModel):
    """Item in cart."""
    item_id: str
    quantity: int = 1


class CartRequest(BaseModel):
    """Cart contents."""
    items: List[CartItem]


class CartSummary(BaseModel):
    """Cart summary with intelligence."""
    total_price: float
    total_items: int
    nutrition: dict  # {calories, protein, carbs, fat}
    health_score: float
    nutrition_gaps: List[str]
    macro_ratios: dict


class CartAddOns(BaseModel):
    """Add-on suggestions."""
    gaps: List[str]
    suggestions: List[dict]  # [{item_name, item_id, reason}]


@router.post("/summary", response_model=CartSummary)
async def get_cart_summary(request: CartRequest):
    """
    Get intelligent cart summary.
    Shows nutrition, health score, gaps, suggestions.
    """
    items_expanded = []
    total_price = 0.0

    # Find full item data
    for cart_item in request.items:
        menu_item = next(
            (i for i in MOCK_MENU if i["id"] == cart_item.item_id),
            None
        )
        if not menu_item:
            raise HTTPException(status_code=404, detail=f"Item {cart_item.item_id} not found")

        items_expanded.append({
            "item_id": cart_item.item_id,
            "quantity": cart_item.quantity
        })
        total_price += menu_item["price"] * cart_item.quantity

    # Calculate nutrition
    nutrition = nutrition_engine.calculate_cart_nutrition(items_expanded)
    health_score = nutrition_engine.health_score(nutrition)
    macro_ratios = nutrition_engine.macro_ratios(nutrition)

    # Detect gaps
    gaps = nutrition_engine.detect_nutrition_gaps(nutrition)

    return CartSummary(
        total_price=round(total_price, 2),
        total_items=sum(i.quantity for i in request.items),
        nutrition=nutrition,
        health_score=health_score,
        nutrition_gaps=gaps,
        macro_ratios=macro_ratios
    )


@router.post("/suggested-addons")
async def get_suggested_addons(
    request: CartRequest,
    user_goal: str = "balanced"
):
    """
    Get intelligent add-on suggestions based on nutrition gaps.
    """
    # Calculate current nutrition
    items_expanded = []
    for cart_item in request.items:
        items_expanded.append({
            "item_id": cart_item.item_id,
            "quantity": cart_item.quantity
        })

    nutrition = nutrition_engine.calculate_cart_nutrition(items_expanded)
    gaps = nutrition_engine.detect_nutrition_gaps(nutrition)

    # Get suggestions
    available_items = [
        {"id": item["id"], "name": item["name"]}
        for item in MOCK_MENU
        if item["id"] not in [i.item_id for i in request.items]  # Exclude already in cart
    ]

    suggestions = nutrition_engine.suggest_addons(
        nutrition,
        available_items,
        user_goal=user_goal
    )

    # Enrich suggestions
    enriched = []
    for suggestion in suggestions:
        item = next((i for i in MOCK_MENU if i["name"] == suggestion), None)
        if item:
            item_nutrition = nutrition_engine.get_item_nutrition(item["id"])
            enriched.append({
                "item_id": item["id"],
                "item_name": item["name"],
                "price": item["price"],
                "reason": f"Adds {item_nutrition['protein']}g protein" if user_goal == "health-first" else "Great value",
                "nutrition_benefit": item_nutrition
            })

    return CartAddOns(gaps=gaps, suggestions=enriched[:3])


@router.post("/estimate-delivery")
async def estimate_delivery(request: CartRequest):
    """
    Estimate delivery time based on items in cart.
    Returns earliest delivery across restaurants.
    """
    min_delivery = 999
    fastest_restaurant = None

    for cart_item in request.items:
        menu_item = next(
            (i for i in MOCK_MENU if i["id"] == cart_item.item_id),
            None
        )
        if menu_item and menu_item["delivery_time_mins"] < min_delivery:
            min_delivery = menu_item["delivery_time_mins"]
            fastest_restaurant = menu_item.get("restaurant", "Unknown")

    return {
        "estimated_delivery_mins": min_delivery if min_delivery != 999 else 30,
        "fastest_restaurant": fastest_restaurant,
        "confidence": "high"
    }


@router.post("/complete-order")
async def complete_order(
    request: CartRequest,
    session_token: Optional[str] = Cookie(None)
):
    """
    Complete order and record in memory for future recommendations.
    """
    if not session_token:
        raise HTTPException(status_code=401, detail="Must be logged in to order")

    user_id = session_token[:8]  # Mock user ID

    # Validate items
    order_items = []
    total_price = 0.0

    for cart_item in request.items:
        menu_item = next(
            (i for i in MOCK_MENU if i["id"] == cart_item.item_id),
            None
        )
        if not menu_item:
            raise HTTPException(status_code=404, detail=f"Item not found: {cart_item.item_id}")

        order_items.append({
            "item_id": cart_item.item_id,
            "name": menu_item["name"],
            "price": menu_item["price"],
            "quantity": cart_item.quantity
        })
        total_price += menu_item["price"] * cart_item.quantity

    # Calculate nutrition
    nutrition = nutrition_engine.calculate_cart_nutrition([
        {"item_id": item["item_id"], "quantity": item["quantity"]}
        for item in order_items
    ])

    # Record order in memory
    from services.memory_engine import MemoryEngine
    memory = MemoryEngine()
    
    order_data = {
        "items": order_items,
        "total_price": total_price,
        "nutrition": nutrition
    }
    memory.record_order(user_id, order_data)

    # In production: Call Swiggy API to create actual order
    
    return {
        "status": "success",
        "message": "Order placed successfully",
        "order_id": f"ORDER_{user_id}_{hash(str(order_items)) % 10000}",
        "total_price": round(total_price, 2),
        "estimated_delivery": "30 mins",
        "nutrition_summary": nutrition
    }


@router.post("/price-breakdown")
async def price_breakdown(request: CartRequest):
    """Get itemized price breakdown."""
    breakdown = {
        "items": [],
        "subtotal": 0.0,
        "taxes": 0.0,
        "delivery_fee": 0.0,
        "discount": 0.0,
        "total": 0.0
    }

    for cart_item in request.items:
        menu_item = next(
            (i for i in MOCK_MENU if i["id"] == cart_item.item_id),
            None
        )
        if not menu_item:
            continue

        item_total = menu_item["price"] * cart_item.quantity
        breakdown["items"].append({
            "name": menu_item["name"],
            "price": menu_item["price"],
            "quantity": cart_item.quantity,
            "total": item_total
        })
        breakdown["subtotal"] += item_total

    # Calculate taxes and fees
    breakdown["taxes"] = round(breakdown["subtotal"] * 0.05, 2)  # 5% tax
    breakdown["delivery_fee"] = 30.0 if breakdown["subtotal"] < 200 else 0.0
    breakdown["total"] = round(
        breakdown["subtotal"] + breakdown["taxes"] + breakdown["delivery_fee"],
        2
    )

    return breakdown
