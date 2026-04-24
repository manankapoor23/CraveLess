# CraveLess — Quick Start Guide

##  Get Running in 5 Minutes

### Option 1: Automated Script (Easiest)

```bash
cd /Users/manankapoor/Desktop/CraveLess
bash start.sh
```

This will:
1.  Check Python & Node.js
2.  Create Python virtual environment
3.  Install dependencies
4.  Initialize database
5.  Start backend (port 8000)
6.  Start frontend (port 3000)

Then open: **http://localhost:3000**

---

### Option 2: Manual Setup

#### Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start server
python main.py
```

Backend runs at: **http://localhost:8000**  
API docs at: **http://localhost:8000/docs**

#### Frontend (in new terminal)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs at: **http://localhost:3000**

---

### Option 3: Docker

```bash
docker-compose up
```

Services:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- PostgreSQL: localhost:5432

---

##  Try It Out

1. **Open Frontend**: http://localhost:3000
2. **Click "Try Demo"** (or login with OAuth)
3. **Select a Persona**: Health-First, Budget, etc.
4. **View Top-3 Recommendations** with explanations
5. **Add to Cart** and see nutrition intelligence
6. **Rate Items** to improve recommendations

---

##  API Examples

### Get Top-3 Recommendations

```bash
curl -X POST http://localhost:8000/recommendations/get-top-3 \
  -H "Content-Type: application/json" \
  -d '{
    "persona": "health-first",
    "intent": "high protein",
    "filters": {
      "max_price": 500,
      "max_delivery_mins": 30
    }
  }'
```

### Get Cart Summary

```bash
curl -X POST http://localhost:8000/cart/summary \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {"item_id": "tandoori_chicken", "quantity": 1},
      {"item_id": "garlic_naan", "quantity": 1}
    ]
  }'
```

### View API Documentation

Open: **http://localhost:8000/docs**

---

##  Troubleshooting

### Port Already in Use
```bash
# Change port in backend/main.py
# Or kill existing process:
lsof -i :8000  # Find process
kill -9 <PID>
```

### Database Error
```bash
# Reset database
rm craveless.db  # SQLite
# Or recreate PostgreSQL database
```

### Frontend Can't Connect to Backend
Check `.env` in frontend folder:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

##  Project Structure

```
CraveLess/
 backend/           # FastAPI server
 frontend/          # Next.js app
 README.md         # Full documentation
 ARCHITECTURE.md   # System design
 API.md           # API reference
 start.sh         # Quick start script
 docker-compose.yml
```

---

##  Next Steps

1. **Explore Mock Data**: Check [backend/data/mock_menu.py](backend/data/mock_menu.py)
2. **Test Personas**: Try all 5 decision personas
3. **Read Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md)
4. **Check API Docs**: Visit `/docs` at running backend
5. **Add Features**: See [DEVELOPMENT.md](DEVELOPMENT.md)

---

##  Key Concepts

### Decision Engine
Scores items across 5 dimensions:
-  Preference match (user history)
-  Health score (nutrition)
-  Price
-  Delivery time
-  Novelty

### Personas
5 dynamic modes that adjust weights:
-  **Balanced** (default)
-  **Health-First** (40% health score)
-  **Budget** (45% price)
-  **Fast Delivery** (40% delivery time)
-  **Explore** (30% novelty)

### Taste Graph
Graph-based preference modeling:
- Nodes: ingredients, cuisines, attributes
- Edges: relationships with propagation
- Finds similar items intelligently

---

##  Support

- **API Docs**: http://localhost:8000/docs
- **Swagger UI**: Interactive API testing
- **GitHub Issues**: Report bugs
- **README**: Full documentation

---

##  Tips

- Use Chrome DevTools to inspect API calls
- API returns explanations for each recommendation
- "Never again" marks items to hide
- Rate items to improve future recommendations
- Switch personas to see ranking changes

---

**Enjoy CraveLess! **
