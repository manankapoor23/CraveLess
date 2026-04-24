"""
CraveLess AI Agent Service (Simplified)
Orchestrates decision making using existing services as tools.
"""

import json
from typing import Optional, Any, List, Dict
from pydantic import BaseModel

from services.ranking_engine import RankingEngine
from services.taste_graph import TasteGraph
from services.memory_engine import MemoryEngine
from services.nutrition_engine import NutritionEngine
from data.mock_menu import MOCK_MENU


class ConversationMessage(BaseModel):
    """Message in agent conversation."""
    role: str  # "user" or "assistant"
    content: str


class AgentResponse(BaseModel):
    """Response from agent."""
    message: str
    recommendations: Optional[List[Dict[str, Any]]] = None
    reasoning: Optional[str] = None
    tools_used: Optional[List[str]] = []


class CraveLessAgent:
    """AI Agent for intelligent food recommendations."""
    
    def __init__(self, user_id: Optional[str] = None):
        """Initialize agent with services."""
        self.user_id = user_id or "default_user"
        
        # Initialize services
        self.ranking_engine = RankingEngine()
        self.taste_graph = TasteGraph()
        self.memory_engine = MemoryEngine()
        self.nutrition_engine = NutritionEngine()
        
        # Conversation history
        self.conversation_history: List[ConversationMessage] = []
        
        # Last determined persona
        self.current_persona = "balanced"
    
    def _parse_intent(self, message: str) -> Dict[str, Any]:
        """Parse user intent from natural language."""
        intent = {
            "health_focused": False,
            "budget_focused": False,
            "speed_focused": False,
            "explore_mode": False,
        }
        
        msg_lower = message.lower()
        
        # Health intent
        if any(word in msg_lower for word in ["healthy", "health", "nutrition", "protein", "diet", "fit", "gym"]):
            intent["health_focused"] = True
        
        # Budget intent
        if any(word in msg_lower for word in ["cheap", "budget", "under", "dollar", "affordable"]):
            intent["budget_focused"] = True
        
        # Speed intent
        if any(word in msg_lower for word in ["quick", "fast", "busy", "hurry", "asap"]):
            intent["speed_focused"] = True
        
        # Explore intent
        if any(word in msg_lower for word in ["new", "try", "explore", "different", "surprise"]):
            intent["explore_mode"] = True
        
        return intent
    
    def _select_persona(self, intent: Dict[str, Any]) -> str:
        """Select persona based on intent."""
        if intent["health_focused"]:
            return "health-first"
        elif intent["budget_focused"]:
            return "budget"
        elif intent["speed_focused"]:
            return "fast-delivery"
        elif intent["explore_mode"]:
            return "explore"
        else:
            return "balanced"
    
    def _get_recommendations(self, persona: str) -> List[Dict]:
        """Get recommendations based on persona."""
        recommendations = self.ranking_engine.get_top_3_with_explanation(
            MOCK_MENU,
            persona=persona.lower()
        )
        return recommendations
    
    def chat(self, user_message: str) -> AgentResponse:
        """Process user message and return agentic response."""
        
        # Parse intent
        intent = self._parse_intent(user_message)
        
        # Select persona
        persona = self._select_persona(intent)
        self.current_persona = persona
        
        # Get recommendations
        recommendations = self._get_recommendations(persona)
        
        # Build response message
        response_parts = []
        
        # Acknowledge intent
        if intent["health_focused"]:
            response_parts.append("Great! You're looking for healthy options.")
        elif intent["budget_focused"]:
            response_parts.append("Looking for affordable choices?")
        elif intent["speed_focused"]:
            response_parts.append("Let me find something quick for you!")
        elif intent["explore_mode"]:
            response_parts.append("Let's explore something new!")
        else:
            response_parts.append("Let me find the best match for you.")
        
        response_parts.append(f"\nUsing {persona.title()} persona:\n")
        
        # Add recommendations
        for rec in recommendations:
            response_parts.append(f"{rec['rank']}. {rec['item']['name']}")
            response_parts.append(f"   Score: {rec['score']:.2f}/10")
            response_parts.append(f"   Why: {rec['explanation']}")
            response_parts.append("")
        
        message = "\n".join(response_parts)
        
        # Store in conversation history
        self.conversation_history.append(ConversationMessage(role="user", content=user_message))
        self.conversation_history.append(ConversationMessage(role="assistant", content=message))
        
        return AgentResponse(
            message=message,
            recommendations=recommendations,
            reasoning=f"Persona selected: {persona}",
            tools_used=["parse_intent", "select_persona", "rank_items"]
        )
    
    def reset_memory(self):
        """Clear conversation history."""
        self.conversation_history = []
    
    def get_history(self) -> List[ConversationMessage]:
        """Get conversation history."""
        return self.conversation_history


# Singleton agent instance
_agent_instance: Optional[CraveLessAgent] = None


def get_agent(user_id: Optional[str] = None) -> CraveLessAgent:
    """Get or create agent instance."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = CraveLessAgent(user_id)
    elif user_id and user_id != _agent_instance.user_id:
        _agent_instance = CraveLessAgent(user_id)
    return _agent_instance
