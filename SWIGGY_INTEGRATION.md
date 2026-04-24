# Swiggy API Integration Guide

This document explains how to integrate CraveLess with real Swiggy APIs when you're ready.

## Current State (Mock Data)

Currently, CraveLess uses mock menu data from `data/mock_menu.py` for development and testing. This allows:
- Full agentic functionality without external dependencies
- Fast development and iteration
- No API rate limits or costs
- Perfect for testing the AI decision logic

## Future Integration with Swiggy MCP Servers

Swiggy provides **three MCP (Model Context Protocol) servers** that can be directly integrated into your agent's tools:

### 1. Swiggy Food (Primary for CraveLess)
Perfect for food delivery recommendations:
```
search_restaurants(query: string) -> List[Restaurant]
search_menu(restaurant_id: string, query: string) -> List[MenuItem]
get_restaurant_menu(restaurant_id: string) -> Menu
update_food_cart(user_id: string, items: List[Item]) -> Cart
get_food_cart(user_id: string) -> Cart
place_food_order(user_id: string, cart: Cart) -> Order
track_food_order(order_id: string) -> OrderStatus
```

### 2. Swiggy Instamart (Grocery Extension)
For instant grocery delivery:
```
search_products(query: string) -> List[Product]
update_cart(user_id: string, items: List[Item]) -> Cart
get_cart(user_id: string) -> Cart
checkout(user_id: string) -> Order
track_order(order_id: string) -> OrderStatus
get_orders(user_id: string) -> List[Order]
```

### 3. Swiggy Dineout (Future: Dining Extension)
For restaurant table bookings:
```
search_restaurants_dineout(query: string) -> List[Restaurant]
get_restaurant_details(restaurant_id: string) -> RestaurantDetails
get_available_slots(restaurant_id: string, date: string) -> List[Slot]
book_table(user_id: string, restaurant_id: string, slot: Slot) -> Booking
get_booking_status(booking_id: string) -> BookingStatus
```

## How to Integrate

### Step 1: Update Agent Tools (Minimal Change)

Current tool structure in `backend/services/agent.py`:

```python
def search_menu_tool(query: str) -> str:
    """Search menu by cuisine, ingredient, or item name."""
    # CURRENT: Searches mock MOCK_MENU
    results = [i for i in MOCK_MENU if query_lower in i['name'].lower()]
    
    # FUTURE: Call Swiggy API instead
    # results = swiggy_client.search_menu(query)
    return json.dumps(results)
```

### Step 2: Create Swiggy Client Wrapper

Create `backend/integrations/swiggy_client.py`:

```python
"""Swiggy API client wrapper for agent tools."""

class SwiggyFoodClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.mcp_server = SwiggyMCPServer(api_key)
    
    def search_menu(self, query: str) -> List[MenuItem]:
        """Use Swiggy Food MCP server."""
        return self.mcp_server.search_menu(query)
    
    def get_restaurant_menu(self, restaurant_id: str) -> Menu:
        return self.mcp_server.get_restaurant_menu(restaurant_id)
    
    def place_order(self, user_id: str, items: List[Item]) -> Order:
        return self.mcp_server.place_food_order(user_id, items)
    
    def track_order(self, order_id: str) -> OrderStatus:
        return self.mcp_server.track_food_order(order_id)


class SwiggyInstamartClient:
    """For grocery orders."""
    def search_products(self, query: str) -> List[Product]:
        return self.mcp_server.search_products(query)


class SwiggyDineoutClient:
    """For restaurant reservations."""
    def search_restaurants(self, query: str) -> List[Restaurant]:
        return self.mcp_server.search_restaurants_dineout(query)
```

### Step 3: Update Agent to Use Swiggy Client

Modify `backend/services/agent.py`:

```python
from integrations.swiggy_client import SwiggyFoodClient

class CraveLessAgent:
    def __init__(self, user_id: Optional[str] = None, use_swiggy: bool = False):
        # ... existing code ...
        
        # Optional: Use real Swiggy APIs
        if use_swiggy:
            swiggy_key = os.getenv("SWIGGY_API_KEY")
            self.menu_client = SwiggyFoodClient(swiggy_key)
        else:
            self.menu_client = MockMenuClient()  # Keep mock as fallback
    
    def _define_tools(self) -> List[Tool]:
        def search_menu_tool(query: str) -> str:
            # Works with both mock and real APIs
            results = self.menu_client.search_menu(query)
            return json.dumps(results)
```

### Step 4: Environment Configuration

Add to `.env`:

```env
# Swiggy Integration (Optional)
USE_SWIGGY_API=false
SWIGGY_API_KEY=your_swiggy_api_key
SWIGGY_MCP_SERVER_URL=your_mcp_server_url
```

### Step 5: Update Nutrition Data

Current: Mock nutrition data for 15 items
Future: Pull nutrition from Swiggy API responses

```python
# CURRENT: static NUTRITION_DATA dict
NUTRITION_DATA = {
    'biryani': {'calories': 450, 'protein': 20, ...}
}

# FUTURE: Dynamic from API
def get_nutrition_from_swiggy(item_id: str):
    menu_item = swiggy_client.get_item_details(item_id)
    return {
        'calories': menu_item.nutrition.calories,
        'protein': menu_item.nutrition.protein,
        ...
    }
```

## Migration Timeline

**Phase 1 (Current)**: Mock data only
- Full agentic functionality ✓
- No external dependencies ✓
- Easy testing ✓

**Phase 2 (Recommended)**: Add Swiggy Food
- Real restaurant menu data
- Real ordering capability
- Keep mock as fallback

**Phase 3 (Optional)**: Add Swiggy Instamart
- Grocery recommendations
- Bundle food + grocery orders

**Phase 4 (Optional)**: Add Swiggy Dineout
- Dining reservations
- Table booking through agent

## Testing Strategy

### Unit Tests (No API Calls)
```python
def test_agent_with_mock_data():
    agent = CraveLessAgent(use_swiggy=False)
    response = agent.chat("I want spicy Indian food under $10")
    assert "recommendations" in response
```

### Integration Tests (With Swiggy APIs)
```python
def test_agent_with_swiggy():
    agent = CraveLessAgent(use_swiggy=True)
    response = agent.chat("What's available near me?")
    # Should query real Swiggy API
    assert response.recommendations
```

## Key Design Points

1. **Interface Abstraction**: Both mock and real clients implement same interface
2. **Fallback Strategy**: Can switch between mock and real data with one env var
3. **No Agent Changes**: Agent logic works identically with both
4. **Extensibility**: Easy to add other food delivery APIs (Zomato, DoorDash, etc.)

## Benefits of This Approach

✓ Test agentic logic without Swiggy credentials
✓ Easy rollback if API changes
✓ Support multiple API providers simultaneously
✓ Zero production cost during development
✓ Agent stays focused on decision-making, not API details
✓ Real data integration when ready

## Resources

- Swiggy MCP Servers: [Swiggy Toolkit Documentation]
- LangChain Tool Integration: https://python.langchain.com/docs/modules/tools/
- Agent Framework: https://python.langchain.com/docs/modules/agents/

## Questions?

For now, focus on perfecting the agentic decision logic. The API integration is a drop-in replacement, not a rewrite.
