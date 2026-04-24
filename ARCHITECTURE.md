# CraveLess Architecture

## System Overview

```
User Browser (Frontend)
    ↓ HTTP/REST
FastAPI Backend
     Auth Service (OAuth)
     Ranking Engine (Multi-objective)
     Taste Graph (Preference propagation)
     Memory Engine (User preferences)
     Nutrition Engine (Health scoring)
    ↓
Database (PostgreSQL/SQLite)
```

## Decision Flow

```
User Request
    ↓
Parse Intent & Filters
    ↓
Load User Preferences (MemoryEngine)
    ↓
Filter Menu Items
    ↓
Score Items (RankingEngine)
     Preference Match (MemoryEngine)
     Health Score (NutritionEngine)
     Price Score
     Delivery Score
     Novelty Score
    ↓
Apply Persona Weights
    ↓
Sort & Select Top 3
    ↓
Explain Results
     Memory signals ("you loved this before")
     Nutritional benefits
     Why recommended
     Similar alternatives
    ↓
Return to Frontend
```

## Component Responsibilities

### RankingEngine
- Multi-objective scoring
- Persona-based weight application
- Final ranking and selection

### TasteGraph
- Node/edge management
- Relationship propagation
- Alternative finding
- Similarity scoring

### MemoryEngine
- Preference storage
- Order history tracking
- Memory signal generation
- Recency weighting

### NutritionEngine
- Nutrition profile lookup
- Cart nutrition calculation
- Health score computation
- Macro ratio analysis

## Data Flow: Get Top-3 Recommendations

1. **Request**: User sends persona + filters
2. **Auth**: Verify session and get user_id
3. **Filter**: Apply price, delivery time, dietary filters
4. **Memory**: Load user's past preferences
5. **Score**: RankingEngine scores all items
6. **Rank**: Sort by score, apply persona weights
7. **Select**: Get top 3 recommendations
8. **Enrich**: Add nutrition, memory signals, explanations
9. **Return**: Send JSON response with top 3

## Data Flow: Record Preference

1. **Request**: User rates an item (e.g., 5/5)
2. **Auth**: Verify session
3. **Memory**: Record preference in MemoryEngine
4. **Graph**: Propagate through TasteGraph
5. **Confirm**: Return success response

## Extensibility Points

### Add New Persona
Edit `PERSONA_WEIGHTS` dictionary with new weight distribution

### Add New Scoring Factor
1. Add to `_*_score()` methods in RankingEngine
2. Add weight to PERSONA_WEIGHTS
3. Document impact

### Add New Item Type
1. Extend MOCK_MENU or database
2. Ensure nutrition data available
3. Optionally add to TasteGraph

### Change Ranking Formula
Modify weighted sum in `score_item()` method

---

This architecture prioritizes:
- **Modularity**: Each service has one responsibility
- **Extensibility**: Easy to add personas, scores, items
- **Testability**: Services work independently
- **Performance**: Fast in-memory operations
