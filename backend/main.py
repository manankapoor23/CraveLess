"""
CraveLess - AI Food Decision Engine
Main FastAPI application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os

from db.database import init_db
from routes import auth, recommendations, cart

# Initialize FastAPI app
app = FastAPI(
    title="CraveLess API",
    description="AI-powered food decision engine with agentic recommendations",
    version="0.1.0"
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize database
@app.on_event("startup")
async def startup():
    """Initialize database and print startup info."""
    init_db()
    print("✅ CraveLess backend started")
    print("📝 API Docs: http://localhost:8000/docs")
    print("🔐 OAuth: /auth/login")
    print("🎯 Recommendations: /recommendations/get-top-3")
    print("🛒 Cart: /cart/summary")


# Include routes
app.include_router(auth.router)
app.include_router(recommendations.router)
app.include_router(cart.router)


@app.get("/")
async def root():
    """Health check and API info."""
    return {
        "app": "CraveLess - AI Food Decision Engine",
        "status": "running",
        "version": "0.1.0",
        "docs": "/docs",
        "endpoints": {
            "auth": "/auth/login (POST) - Initiate OAuth flow",
            "recommendations": "/recommendations/get-top-3 (POST) - Get top-3 recommendations",
            "cart": "/cart/summary (POST) - Get cart intelligence"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/about")
async def about():
    """About CraveLess."""
    return {
        "name": "CraveLess",
        "tagline": "AI Food Decision Engine",
        "description": "Intelligent recommendation system powered by agentic decision-making",
        "features": [
            "Top-3 personalized recommendations",
            "Taste graph modeling",
            "Multi-objective optimization (preference, price, health, delivery, novelty)",
            "Cart intelligence with nutrition tracking",
            "OAuth integration",
            "Decision personas: health-first, budget, fast-delivery, explore, balanced"
        ],
        "architecture": {
            "backend": "FastAPI + Python",
            "frontend": "Next.js + React",
            "database": "PostgreSQL (with SQLite fallback)",
            "engines": ["RankingEngine", "TasteGraph", "MemoryEngine", "NutritionEngine"]
        }
    }


# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc)
        }
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
