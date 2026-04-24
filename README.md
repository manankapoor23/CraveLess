# CraveLess — AI Food Decision Engine

A production-ready agentic system that solves decision fatigue in food ordering through intelligent, intent-driven recommendations.

## 🎯 Problem Statement

Current food delivery platforms optimize for **exploration**, not **decision-making**:
- Users scroll endlessly through options
- Too many choices lead to indecision
- Valuable time wasted comparing similar items
- No understanding of user intent or preferences

**CraveLess** replaces exploration with **intent-driven decision-making**:
→ Top-3 optimized recommendations  
→ Intelligent execution  
→ Preference memory that improves over time

---

## ✨ Core Features

### 1. **Decision Engine**
- Multi-objective scoring across 5 dimensions:
  - Preference match (user history)
  - Price optimization
  - Delivery time
  - Health score
  - Novelty (explore new items)
- Top-3 recommendation system with explanations

### 2. **Preference Memory**
- Stores: likes, dislikes, past orders, "never again" items
- Memory-aware feedback: "you loved this before", "you didn't like this"
- Integrated into all ranking decisions

### 3. **Taste Graph** (Core Differentiator)
- Graph-based preference modeling
- Nodes: ingredients, cuisines, attributes, brands
- Edges: relationships with propagation strength
- Propagates preferences through the graph for related items
- Finds intelligent alternatives and similar items

### 4. **Cart Intelligence**
- Real-time nutrition tracking: calories, protein, carbs, fat
- Health score calculation (0-10)
- Automatic detection of nutrition gaps
- Smart add-on suggestions based on gaps and taste

### 5. **Decision Personas**
Dynamic mode switching:
- **Health-First**: Prioritizes nutrition (40% weight)
- **Budget**: Optimizes for price (45% weight)
- **Fast Delivery**: Minimizes delivery time (40% weight)
- **Explore**: Maximizes novelty (30% weight)
- **Balanced**: Equal weighting across all factors (default)

### 6. **OAuth Integration**
- Backend-driven OAuth flow with full state validation
- Support for Google, Swiggy, and other OAuth providers
- HTTP-only cookies for security
- Automatic session management

### 7. **Nutrition Engine**
- Item-level nutrition profiles
- Cart-level macro ratios
- Health scoring algorithm
- Personalized add-on recommendations

---

## 🏗️ Architecture

### **Backend: FastAPI + Python**

```
/backend
  /routes          → API endpoints (auth, recommendations, cart)
  /services        → Core business logic
    - ranking_engine.py    (Multi-objective scoring)
    - taste_graph.py       (Graph-based preferences)
    - memory_engine.py     (User preference tracking)
    - nutrition_engine.py  (Health & nutrition scoring)
  /models          → SQLAlchemy database models
  /db              → Database setup and session management
  /data            → Mock data for quick start
  main.py          → FastAPI app initialization
```

**Key Services:**
1. **RankingEngine**: Multi-objective optimization with persona-based weights
2. **TasteGraph**: Graph propagation, similarity finding, alternative suggestions
3. **MemoryEngine**: Preference storage, order history, recency weighting
4. **NutritionEngine**: Calorie/macro calculation, health scoring, add-on recommendations

### **Frontend: Next.js + React**

```
/frontend
  /pages
    - index.js          (Landing page with login)
    - dashboard.js      (Main recommendation interface)
  /components
    - RecommendationCard.js  (Individual recommendation display)
    - CartSummary.js         (Cart intelligence dashboard)
  /styles
    - globals.css       (Global styling)
```

### **Database: PostgreSQL** (with SQLite fallback)

Models:
- `User`: OAuth credentials, preferences, dietary restrictions
- `Preference`: User ratings and preferences per item
- `Order`: Past orders with nutrition summaries
- `TasteGraphNode`: Ingredients, cuisines, attributes
- `TasteGraphEdge`: Relationships in taste graph

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL (optional; SQLite used by default)

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
cp ../.env.example ../.env

# Initialize database
python -c "from db.database import init_db; init_db()"

# Start server
python main.py
```

Server runs on `http://localhost:8000`  
API docs available at `http://localhost:8000/docs`

### 2. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env.local (if needed)
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start development server
npm run dev
```

Frontend runs on `http://localhost:3000`

### 3. Try the Demo

1. Open `http://localhost:3000`
2. Click "Try Demo" or login with OAuth
3. Select a persona (Health-First, Budget, etc.)
4. View top-3 recommendations with explanations
5. Add items to cart and see nutrition intelligence

---

## 📊 API Endpoints

### Authentication
- `POST /auth/login` — Initiate OAuth flow
- `POST /auth/callback` — Handle OAuth callback
- `GET /auth/me` — Get current user
- `POST /auth/logout` — Logout
- `POST /auth/refresh` — Refresh session

### Recommendations (Core)
- `POST /recommendations/get-top-3` — Get personalized top-3 recommendations
  - Request: `{persona, intent, filters}`
  - Response: Top-3 items with explanations and nutrition
  
- `POST /recommendations/record-preference` — Record user rating
- `POST /recommendations/never-again` — Mark item "never show again"
- `GET /recommendations/similar/{item_id}` — Find similar items via taste graph
- `GET /recommendations/persona-comparison` — Compare rankings across all personas

### Cart Intelligence
- `POST /cart/summary` — Get cart nutrition, health score, gaps
- `POST /cart/suggested-addons` — Get smart add-on recommendations
- `POST /cart/estimate-delivery` — Estimate delivery time
- `POST /cart/complete-order` — Place order and record in memory
- `POST /cart/price-breakdown` — Itemized pricing

---

## 🧠 Core Algorithms

### Multi-Objective Ranking

Final Score = (preference_match × w1) + (health × w2) + (price × w3) + (delivery × w4) + (novelty × w5)

Where weights vary by persona:
- **Health-First**: [0.25, 0.40, 0.15, 0.10, 0.10]
- **Budget**: [0.30, 0.10, 0.45, 0.10, 0.05]
- **Fast Delivery**: [0.30, 0.10, 0.15, 0.40, 0.05]
- **Explore**: [0.20, 0.15, 0.20, 0.15, 0.30]
- **Balanced**: [0.30, 0.20, 0.20, 0.15, 0.15]

### Taste Graph Propagation

When a user rates an item:
1. Find all related nodes (ingredients, cuisines, attributes)
2. Propagate preference with decay based on distance
3. Update memory for related items
4. Use for future ranking

### Health Score Calculation

```
Health Score = (0.4 × protein_score) + (0.4 × calorie_score) + (0.2 × fat_score)
Range: 0-10
```

---

## 📦 Mock Data

Backend includes mock menu with 15+ restaurant items across cuisines:
- Indian (Biryani, Paneer, Dal Makhani, etc.)
- Chinese (Fried Rice, Ramen)
- Italian (Pizza)
- Seafood (Grilled Fish)
- Health (Buddha Bowl, Açai Bowl)
- Desserts

Each item includes:
- Name, description, price, delivery time
- Nutrition (calories, protein, carbs, fat)
- Health score, ratings, cuisine tags
- Allergen information

---

## 🔧 Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=sqlite:///./craveless.db
# For PostgreSQL: postgresql://user:password@localhost/craveless

# OAuth
GOOGLE_CLIENT_ID=xxx
SWIGGY_CLIENT_ID=yyy

# API
API_PORT=8000
DEBUG=False
```

---

## 🎨 Persona System

Users can dynamically switch personas:

| Persona | Focus | Use Case |
|---------|-------|----------|
| 🎯 **Balanced** | Equal across all factors | Default, everyday ordering |
| 💪 **Health-First** | Nutrition, protein | Fitness-focused users |
| 💰 **Budget** | Price optimization | Cost-conscious users |
| ⚡ **Fast Delivery** | Delivery speed | Time-constrained users |
| 🔍 **Explore** | Novelty, new items | Adventure-seeking users |

---

## 🚧 Future Improvements

### Phase 2: Advanced Features
- [ ] Real Swiggy MCP API integration
- [ ] Real-time inventory and pricing updates
- [ ] User subscription for preferences persistence
- [ ] Collaborative filtering (learn from similar users)
- [ ] Advanced NLP for intent parsing ("high protein + spicy + <₹300")
- [ ] Seasonal recommendations
- [ ] Time-of-day personalization
- [ ] Estimated macro recommendations for fitness goals

### Phase 3: Production Hardening
- [ ] Redis for session/cache management
- [ ] Comprehensive testing suite
- [ ] Performance optimization and caching
- [ ] Analytics and usage tracking
- [ ] Admin dashboard for data management
- [ ] Rate limiting and DDoS protection
- [ ] Mobile app (React Native)

### Phase 4: AI Enhancements
- [ ] LLM-powered intent understanding (Claude, GPT)
- [ ] Computer vision for food image recognition
- [ ] Voice-based ordering
- [ ] Contextual recommendations (weather, events, etc.)
- [ ] Predictive ordering based on patterns

---

## 🛠️ Development

### Adding New Personas

Edit [ranking_engine.py](backend/services/ranking_engine.py):

```python
PERSONA_WEIGHTS = {
    "my-persona": {
        "preference_match": 0.30,
        "health_score": 0.30,
        "price": 0.20,
        "delivery_time": 0.10,
        "novelty": 0.10
    }
}
```

### Adding Menu Items

Edit [mock_menu.py](backend/data/mock_menu.py) and add items to `MOCK_MENU` list with structure:

```python
{
    "id": "unique_id",
    "name": "Item Name",
    "category": "cuisine",
    "price": 300,
    "delivery_time_mins": 20,
    "health_score": 7.5,
    # ... more fields
}
```

### Extending Taste Graph

Modify [taste_graph.py](backend/services/taste_graph.py) initialization:

```python
self.add_node("ingredient", type="ingredient")
self.add_edge("ingredient1", "ingredient2", strength=0.8)
```

---

## 📝 Testing

Quick manual testing:

```bash
# Get top-3 recommendations
curl -X POST http://localhost:8000/recommendations/get-top-3 \
  -H "Content-Type: application/json" \
  -d '{"persona": "health-first"}'

# Record preference
curl -X POST http://localhost:8000/recommendations/record-preference \
  -d "item_id=chicken_biryani&rating=5"

# Get cart summary
curl -X POST http://localhost:8000/cart/summary \
  -H "Content-Type: application/json" \
  -d '{"items": [{"item_id": "chicken_biryani", "quantity": 1}]}'
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License - see LICENSE file for details

---

## 👨‍💻 Author

CraveLess Team  
Built with ❤️ to eliminate food ordering decision fatigue

---

## 📞 Support

- Documentation: `/docs` (Swagger UI)
- Issues: GitHub Issues
- Email: support@craveless.io

---

## 🎯 Vision

CraveLess is not just a food delivery app. It's a **decision intelligence system** that understands:
- **What users want** (intent parsing)
- **What users like** (preference memory)
- **What's healthy** (nutrition modeling)
- **What's available** (real-time inventory)
- **What's optimal** (multi-objective ranking)

Our goal: **Make food ordering effortless by replacing endless choice with intelligent curation.**
