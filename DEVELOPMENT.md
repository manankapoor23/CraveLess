# CraveLess Development Guide

## Project Structure

```
craveless/
 backend/
    main.py                 # FastAPI app entry point
    requirements.txt         # Python dependencies
    routes/
       auth.py            # OAuth endpoints
       recommendations.py  # Core recommendation endpoint
       cart.py            # Cart & order endpoints
    services/
       ranking_engine.py   # Multi-objective scoring
       taste_graph.py      # Graph-based preferences
       memory_engine.py    # User preference tracking
       nutrition_engine.py # Health & nutrition
    models/
       user.py            # User model with OAuth
       preference.py       # Preference & order models
    db/
       database.py        # SQLAlchemy config
    data/
        mock_menu.py       # Mock restaurant data

 frontend/
    pages/
       index.js           # Landing page
       dashboard.js       # Main interface
       _app.js            # App wrapper
    components/
       RecommendationCard.js
       CartSummary.js
    styles/
       globals.css
    package.json
    next.config.js

 .env.example
 README.md
```

## Quick Start Commands

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Key Design Decisions

1. **FastAPI**: Modern, fast, great OpenAPI support
2. **SQLAlchemy**: Flexible ORM, easy to switch databases
3. **In-Memory Engines**: MemoryEngine and RankingEngine for quick iteration
4. **Mock Data**: Works without real APIs for demo/testing
5. **Persona-Based Weights**: Extensible ranking system
6. **Taste Graph**: Enables intelligent preference propagation

## Common Tasks

### Add a New Persona
Edit `PERSONA_WEIGHTS` in `services/ranking_engine.py`

### Add Menu Items
Edit `MOCK_MENU` list in `data/mock_menu.py`

### Add Database Model
1. Create model in `models/`
2. Update `db/database.py`
3. Run initialization

### Test Endpoints
Use `/docs` (Swagger UI) at http://localhost:8000/docs

## Next Steps

1. **Real Data**: Replace mock menu with actual Swiggy API
2. **Database**: Switch from SQLite to PostgreSQL
3. **Persistence**: Migrate MemoryEngine to database queries
4. **Authentication**: Implement real OAuth flows
5. **Testing**: Add pytest suite
6. **Deployment**: Docker, environment configs
