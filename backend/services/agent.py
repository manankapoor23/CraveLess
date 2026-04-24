"""
CraveLess AI Agent Service
Orchestrates LLM-based decision making using existing services as tools.
"""

import json
import os
from typing import Optional, Any, List, Dict
from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
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
    tools_used: Optional[List[str]] = None


class CraveLessAgent:
    """AI Agent for intelligent food recommendations."""
    
    def __init__(self, user_id: Optional[str] = None):
        """Initialize agent with services and LLM."""
        self.user_id = user_id or "default_user"
        
        # Initialize services
        self.ranking_engine = RankingEngine()
        self.taste_graph = TasteGraph()
        self.memory_engine = MemoryEngine()
        self.nutrition_engine = NutritionEngine()
        
        # Initialize LLM
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set in environment")
        
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=api_key,
            streaming=False
        )
        
        # Initialize conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            human_prefix="User",
            ai_prefix="Agent"
        )
        
        # Define tools
        self.tools = self._define_tools()
        
        # Initialize agent
        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent="chat-conversational-react-description",
            memory=self.memory,
            verbose=True,
            max_iterations=5,
            handle_parsing_errors=True
        )
        
        # System prompt
        self.system_prompt = """You are CraveLess, an intelligent food decision engine designed to help users 
make the best food choices based on their preferences, health goals, and constraints.

Your approach:
1. LISTEN - Understand user intent and constraints
2. THINK - Use available tools to gather information about options
3. RECOMMEND - Provide personalized recommendations with clear reasoning
4. EXPLAIN - Help users understand why these choices match their goals

Always:
- Ask clarifying questions if user intent is unclear
- Consider health, taste, budget, and delivery time factors
- Remember user preferences from conversation history
- Be conversational and friendly
- Provide actionable recommendations, not just lists

Available tools help you:
- Search menu and get nutrition info
- Calculate recommendation scores
- Access user taste preferences
- Make final decisions

When recommending, always explain your reasoning clearly."""
    
    def _define_tools(self) -> List[Tool]:
        """Define tools for the agent."""
        
        def search_menu_tool(query: str) -> str:
            """Search menu by cuisine, ingredient, or item name."""
            query_lower = query.lower()
            results = []
            for item in MOCK_MENU:
                if (query_lower in item['name'].lower() or
                    query_lower in item['category'].lower() or
                    query_lower in item['description'].lower() or
                    query_lower in item['cuisine'].lower()):
                    results.append({
                        'id': item['id'],
                        'name': item['name'],
                        'cuisine': item['cuisine'],
                        'price': item['price'],
                        'delivery_time': item['delivery_time_mins'],
                        'rating': item['rating'],
                        'is_new': item['is_new']
                    })
            return json.dumps(results[:10]) if results else "No items found"
        
        def get_nutrition_tool(item_id: str) -> str:
            """Get nutrition information for an item."""
            item = next((i for i in MOCK_MENU if i['id'] == item_id), None)
            if not item:
                return f"Item {item_id} not found"
            
            nutrition = self.nutrition_engine.get_item_nutrition(item_id)
            return json.dumps({
                'name': item['name'],
                'nutrition': nutrition,
                'health_score': self.nutrition_engine.health_score(nutrition),
                'allergens': item.get('allergens', [])
            })
        
        def get_user_preferences_tool(constraint: str) -> str:
            """Get user's taste preferences and history."""
            prefs = self.memory_engine.get_user_preferences(self.user_id)
            recent = self.memory_engine.get_recent_items(self.user_id, limit=5)
            affinity = self.memory_engine.get_category_affinity(self.user_id)
            
            return json.dumps({
                'preferences': prefs,
                'recent_items': recent,
                'category_affinity': affinity,
                'total_orders': len(self.memory_engine.user_order_history.get(self.user_id, []))
            })
        
        def calculate_score_tool(item_ids: str, persona: str = "Balanced") -> str:
            """Calculate recommendation scores for items using persona weights."""
            ids = item_ids.split(',')
            items = [i for i in MOCK_MENU if i['id'] in ids]
            
            scores = []
            for item in items:
                score = self.ranking_engine.score_item(
                    item,
                    persona=persona,
                    user_id=self.user_id
                )
                scores.append({
                    'item_id': item['id'],
                    'name': item['name'],
                    'score': round(score, 2),
                    'price': item['price'],
                    'delivery_time': item['delivery_time_mins']
                })
            
            # Sort by score descending
            scores.sort(key=lambda x: x['score'], reverse=True)
            return json.dumps(scores[:3])
        
        def record_preference_tool(item_id: str, rating: int, notes: str = "") -> str:
            """Record user preference for an item."""
            self.memory_engine.record_preference(
                user_id=self.user_id,
                item_id=item_id,
                rating=rating,
                notes=notes
            )
            item = next((i for i in MOCK_MENU if i['id'] == item_id), None)
            if item:
                return f"Recorded {rating}/5 rating for {item['name']}"
            return "Preference recorded"
        
        def get_taste_graph_tool(cuisine: str) -> str:
            """Get related cuisines and ingredients based on taste graph."""
            related = self.taste_graph.get_related_nodes(cuisine)
            return json.dumps({
                'cuisine': cuisine,
                'related_cuisines': related,
                'suggestion': f"Since you like {cuisine}, you might enjoy these related options"
            })
        
        tools = [
            Tool(
                name="search_menu",
                func=search_menu_tool,
                description="Search menu by cuisine, ingredient, or item name. Input: search query (string)"
            ),
            Tool(
                name="get_nutrition",
                func=get_nutrition_tool,
                description="Get nutrition information and health score for an item. Input: item_id (string)"
            ),
            Tool(
                name="get_user_preferences",
                func=get_user_preferences_tool,
                description="Get user's taste preferences, recent orders, and food affinities. Input: any constraint (string)"
            ),
            Tool(
                name="calculate_score",
                func=calculate_score_tool,
                description="Calculate recommendation scores for items. Input: comma-separated item IDs and optional persona (Balanced, Health-First, Budget, Fast-Delivery, Explore)"
            ),
            Tool(
                name="record_preference",
                func=record_preference_tool,
                description="Record user rating for an item to improve future recommendations. Input: item_id, rating (1-5), optional notes"
            ),
            Tool(
                name="get_taste_graph",
                func=get_taste_graph_tool,
                description="Get related cuisines and ingredients based on user taste patterns. Input: cuisine name (string)"
            )
        ]
        
        return tools
    
    def chat(self, user_message: str) -> AgentResponse:
        """
        Process user message through agent and return response.
        
        Args:
            user_message: User's natural language input
            
        Returns:
            AgentResponse with message, recommendations, and reasoning
        """
        try:
            # Get agent response
            response = self.agent.run(
                input=user_message,
                system_message=self.system_prompt
            )
            
            # Parse response
            return AgentResponse(
                message=response,
                reasoning="Agent processed your request and provided recommendations",
                tools_used=["search_menu", "calculate_score", "get_user_preferences"]
            )
        except Exception as e:
            return AgentResponse(
                message=f"I encountered an issue: {str(e)}. Could you rephrase your request?",
                reasoning=f"Error: {str(e)}"
            )
    
    def reset_memory(self):
        """Clear conversation history."""
        self.memory.clear()
    
    def get_history(self) -> List[ConversationMessage]:
        """Get conversation history."""
        messages = []
        if hasattr(self.memory, 'buffer'):
            for msg in self.memory.buffer:
                if isinstance(msg, dict):
                    messages.append(ConversationMessage(
                        role=msg.get('type', 'user'),
                        content=msg.get('content', '')
                    ))
        return messages


# Singleton agent instance (in production, use per-user instances)
_agent_instance: Optional[CraveLessAgent] = None


def get_agent(user_id: Optional[str] = None) -> CraveLessAgent:
    """Get or create agent instance."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = CraveLessAgent(user_id)
    elif user_id and user_id != _agent_instance.user_id:
        _agent_instance = CraveLessAgent(user_id)
    return _agent_instance
