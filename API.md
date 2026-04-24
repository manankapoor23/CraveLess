# CraveLess API Reference

## Authentication Endpoints

### POST /auth/login
Initiate OAuth flow.

**Request:**
```json
{
  "provider": "google"
}
```

**Response:**
```json
{
  "auth_url": "https://accounts.google.com/o/oauth2/v2/auth?...",
  "state": "uuid-string"
}
```

### POST /auth/callback
Handle OAuth callback.

**Request:**
```json
{
  "code": "authorization_code",
  "state": "uuid-string",
  "provider": "google"
}
```

**Response:**
```json
{
  "status": "success",
  "user": {
    "id": "user_id",
    "email": "user@example.com",
    "name": "John Doe",
    "provider": "google"
  }
}
```

### GET /auth/me
Get current authenticated user.

**Response:**
```json
{
  "id": "user_id",
  "email": "user@example.com",
  "name": "John Doe",
  "provider": "google"
}
```

---

## Recommendations Endpoints

### POST /recommendations/get-top-3
**Get personalized top-3 recommendations (CORE ENDPOINT)**

**Request:**
```json
{
  "persona": "health-first",
  "intent": "high protein",
  "filters": {
    "max_price": 500,
    "max_delivery_mins": 30,
    "dietary_restrictions": ["gluten-free"]
  }
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "rank": 1,
      "item": {
        "id": "tandoori_chicken",
        "name": "Tandoori Chicken",
        "description": "...",
        "price": 280,
        "delivery_time_mins": 15,
        "health_score": 8.2
      },
      "score": 9.2,
      "explanation": "you loved this before, healthy choice, quick delivery",
      "memory_signal": {
        "seen": true,
        "signal": "liked",
        "rating": 5.0,
        "count": 2
      },
      "nutrition": {
        "calories": 165,
        "protein": 28,
        "carbs": 0,
        "fat": 6
      }
    },
    // ... rank 2, rank 3
  ],
  "summary": {
    "intent": "high protein",
    "persona": "health-first",
    "filters_applied": {...},
    "total_items_considered": 15
  }
}
```

### POST /recommendations/record-preference
Record user preference/rating for an item.

**Request:**
```
POST /recommendations/record-preference?item_id=tandoori_chicken&rating=5
```

**Response:**
```json
{
  "status": "success",
  "message": "Preference recorded: Tandoori Chicken = 5/5"
}
```

### POST /recommendations/never-again
Mark item as "never show again".

**Request:**
```
POST /recommendations/never-again?item_id=paneer_butter_masala
```

**Response:**
```json
{
  "status": "success",
  "message": "Paneer Butter Masala will no longer be recommended"
}
```

### GET /recommendations/similar/{item_id}
Get similar items based on taste graph.

**Request:**
```
GET /recommendations/similar/tandoori_chicken?limit=5
```

**Response:**
```json
{
  "original_item_id": "tandoori_chicken",
  "similar_items": [
    {
      "item": {
        "id": "grilled_fish",
        "name": "Grilled Fish",
        ...
      },
      "similarity_score": 0.85
    }
  ]
}
```

### GET /recommendations/persona-comparison
Compare top-3 across all personas.

**Response:**
```json
{
  "persona_comparison": {
    "health-first": [
      {
        "rank": 1,
        "item_name": "Grilled Fish",
        "score": 9.1
      }
    ],
    "budget": [
      {
        "rank": 1,
        "item_name": "Vegetable Fried Rice",
        "score": 8.7
      }
    ],
    // ... all personas
  }
}
```

---

## Cart Endpoints

### POST /cart/summary
Get intelligent cart summary with nutrition and gaps.

**Request:**
```json
{
  "items": [
    {"item_id": "tandoori_chicken", "quantity": 1},
    {"item_id": "garlic_naan", "quantity": 2}
  ]
}
```

**Response:**
```json
{
  "total_price": 440.0,
  "total_items": 3,
  "nutrition": {
    "calories": 785,
    "protein": 36,
    "carbs": 100,
    "fat": 20
  },
  "health_score": 7.2,
  "nutrition_gaps": [
    "Add more vegetables"
  ],
  "macro_ratios": {
    "protein": 20,
    "carbs": 55,
    "fat": 11
  }
}
```

### POST /cart/suggested-addons
Get smart add-on suggestions.

**Request:**
```json
{
  "items": [
    {"item_id": "tandoori_chicken", "quantity": 1}
  ],
  "user_goal": "health-first"
}
```

**Response:**
```json
{
  "gaps": ["Add vegetables", "Add fiber"],
  "suggestions": [
    {
      "item_id": "greek_salad",
      "item_name": "Greek Salad",
      "price": 280,
      "reason": "Adds 8g protein and vegetables",
      "nutrition_benefit": {
        "calories": 150,
        "protein": 8,
        "carbs": 12,
        "fat": 8
      }
    }
  ]
}
```

### POST /cart/estimate-delivery
Estimate delivery time.

**Request:**
```json
{
  "items": [
    {"item_id": "tandoori_chicken", "quantity": 1}
  ]
}
```

**Response:**
```json
{
  "estimated_delivery_mins": 15,
  "fastest_restaurant": "Tandoori King",
  "confidence": "high"
}
```

### POST /cart/complete-order
Place order and record in memory.

**Request:**
```json
{
  "items": [
    {"item_id": "tandoori_chicken", "quantity": 1}
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "order_id": "ORDER_abc12_5678",
  "total_price": 280.0,
  "estimated_delivery": "15 mins",
  "nutrition_summary": {
    "calories": 165,
    "protein": 28,
    "carbs": 0,
    "fat": 6
  }
}
```

### POST /cart/price-breakdown
Get itemized price breakdown.

**Request:**
```json
{
  "items": [
    {"item_id": "tandoori_chicken", "quantity": 1}
  ]
}
```

**Response:**
```json
{
  "items": [
    {
      "name": "Tandoori Chicken",
      "price": 280,
      "quantity": 1,
      "total": 280
    }
  ],
  "subtotal": 280.0,
  "taxes": 14.0,
  "delivery_fee": 0.0,
  "discount": 0.0,
  "total": 294.0
}
```

---

## Utility Endpoints

### GET /
Health check and API info.

### GET /health
Health check.

### GET /about
About CraveLess.

---

## Error Responses

All errors follow this format:

```json
{
  "error": "error_type",
  "detail": "error_message"
}
```

Common HTTP Status Codes:
- `200`: Success
- `400`: Bad request
- `401`: Unauthorized
- `404`: Not found
- `500`: Server error
