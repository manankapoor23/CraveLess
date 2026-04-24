"""
CraveLess Agent API Routes
Conversation and agentic recommendation endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from services.agent import get_agent, AgentResponse

router = APIRouter(prefix="/agent", tags=["agent"])


class ChatRequest(BaseModel):
    """Request body for chat endpoint."""
    message: str
    user_id: Optional[str] = "default_user"


class ChatMessage(BaseModel):
    """Single message in conversation."""
    role: str  # "user" or "assistant"
    content: str


class ChatResponse(BaseModel):
    """Response from chat endpoint."""
    message: str
    recommendations: Optional[List[dict]] = None
    reasoning: Optional[str] = None
    tools_used: Optional[List[str]] = None
    session_id: Optional[str] = None


@router.post("/chat", response_model=ChatResponse)
async def agent_chat(request: ChatRequest):
    """
    Chat with the CraveLess AI agent.
    
    The agent understands natural language requests and provides
    intelligent, personalized food recommendations based on:
    - Your preferences and history
    - Health and nutrition goals
    - Budget and delivery time constraints
    - Taste patterns and affinities
    
    Example requests:
    - "I'm busy today, I need something quick and cheap"
    - "I'm trying to eat healthier, what's a good option?"
    - "Surprise me with something I haven't tried"
    - "Can you suggest something with Indian flavors under $7?"
    
    Args:
        message: Your natural language request
        user_id: Optional user identifier for personalization
        
    Returns:
        Agent response with recommendations and reasoning
    """
    try:
        # Get or create agent for this user
        agent = get_agent(request.user_id)
        
        # Process message through agent
        response = agent.chat(request.message)
        
        return ChatResponse(
            message=response.message,
            recommendations=response.recommendations,
            reasoning=response.reasoning,
            tools_used=response.tools_used,
            session_id=request.user_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Agent error: {str(e)}"
        )


@router.post("/chat/reset")
async def reset_conversation(user_id: Optional[str] = "default_user"):
    """
    Reset conversation history for a user.
    
    Use this to start fresh without the agent remembering
    previous conversation context.
    """
    try:
        agent = get_agent(user_id)
        agent.reset_memory()
        return {
            "status": "success",
            "message": "Conversation history cleared",
            "user_id": user_id
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error resetting conversation: {str(e)}"
        )


@router.get("/chat/history")
async def get_chat_history(user_id: Optional[str] = "default_user"):
    """
    Get conversation history for a user.
    
    Returns all previous messages in the conversation.
    """
    try:
        agent = get_agent(user_id)
        history = agent.get_history()
        return {
            "user_id": user_id,
            "history": history,
            "total_messages": len(history)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving history: {str(e)}"
        )


@router.get("/status")
async def agent_status():
    """Get agent system status and capabilities."""
    return {
        "status": "operational",
        "agent": "CraveLess AI",
        "capabilities": [
            "Natural language understanding",
            "Multi-objective optimization",
            "Personalized recommendations",
            "Nutrition analysis",
            "Taste preference learning",
            "Conversational interface"
        ],
        "tools": [
            "search_menu",
            "get_nutrition",
            "get_user_preferences",
            "calculate_score",
            "record_preference",
            "get_taste_graph"
        ],
        "version": "1.0.0"
    }


@router.post("/recommend")
async def agent_recommend(request: ChatRequest):
    """
    Quick recommendation endpoint.
    
    Same as chat but optimized for quick, one-shot recommendations.
    Just tell the agent what you're in the mood for and get instant results.
    """
    try:
        agent = get_agent(request.user_id)
        response = agent.chat(
            f"Based on my preferences, please recommend 3 items. My request: {request.message}"
        )
        
        return ChatResponse(
            message=response.message,
            recommendations=response.recommendations,
            reasoning=response.reasoning,
            tools_used=response.tools_used,
            session_id=request.user_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Recommendation error: {str(e)}"
        )
