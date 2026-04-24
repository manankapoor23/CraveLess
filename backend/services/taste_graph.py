"""
Taste Graph - Graph-based preference modeling system.
Models relationships between ingredients, cuisines, and attributes.
"""

from typing import List, Dict, Set, Tuple
import json


class TasteGraph:
    """
    Graph-based taste modeling.
    Nodes: ingredients, cuisines, attributes, brands
    Edges: relationships and their strength
    """

    def __init__(self):
        self.nodes: Dict[str, Dict] = {}
        self.edges: Dict[str, Dict[str, float]] = {}
        self._init_base_graph()

    def _init_base_graph(self):
        """Initialize with common food attributes."""
        # Cuisines
        cuisines = ["italian", "indian", "chinese", "mexican", "thai", "japanese"]
        for cuisine in cuisines:
            self.add_node(cuisine, type="cuisine")

        # Common ingredients
        ingredients = [
            "chicken", "fish", "paneer", "tofu",  # proteins
            "rice", "pasta", "bread", "noodles",  # carbs
            "spinach", "broccoli", "tomato", "onion",  # veggies
            "cheese", "garlic", "ginger", "chili"  # flavor
        ]
        for ingredient in ingredients:
            self.add_node(ingredient, type="ingredient")

        # Attributes
        attributes = ["spicy", "mild", "sweet", "savory", "healthy", "indulgent"]
        for attr in attributes:
            self.add_node(attr, type="attribute")

        # Sample relationships
        relationships = [
            ("chicken", "protein", 1.0),
            ("paneer", "protein", 1.0),
            ("indian", "spicy", 0.8),
            ("thai", "spicy", 0.9),
            ("italian", "pasta", 0.8),
            ("healthy", "spinach", 0.9),
            ("indulgent", "cheese", 0.8),
        ]
        for from_node, to_node, strength in relationships:
            self.add_edge(from_node, to_node, strength)

    def add_node(self, node_id: str, type: str = "ingredient", **properties):
        """Add a node to the graph."""
        self.nodes[node_id] = {
            "type": type,
            "properties": properties
        }
        if node_id not in self.edges:
            self.edges[node_id] = {}

    def add_edge(self, from_node: str, to_node: str, strength: float = 1.0):
        """Add an edge between nodes."""
        if from_node not in self.nodes:
            self.add_node(from_node, type="ingredient")
        if to_node not in self.nodes:
            self.add_node(to_node, type="ingredient")
        
        self.edges[from_node][to_node] = strength

    def get_related_nodes(self, node_id: str, depth: int = 2) -> Set[str]:
        """
        Get all related nodes within depth hops.
        Used to propagate preferences.
        """
        related = set()
        visited = set()
        queue = [(node_id, 0)]

        while queue:
            current, current_depth = queue.pop(0)
            if current in visited or current_depth > depth:
                continue
            visited.add(current)
            
            if current != node_id:
                related.add(current)

            if current in self.edges:
                for neighbor in self.edges[current]:
                    if neighbor not in visited:
                        queue.append((neighbor, current_depth + 1))

        return related

    def propagate_preference(self, liked_node: str, preference_value: float) -> Dict[str, float]:
        """
        Propagate a user preference through the graph.
        Returns affected nodes and their adjusted preference values.
        """
        related = self.get_related_nodes(liked_node, depth=2)
        propagated = {liked_node: preference_value}

        for related_node in related:
            # Strength decays based on distance
            strength = self.edges.get(liked_node, {}).get(related_node, 0.5)
            propagated[related_node] = preference_value * strength

        return propagated

    def find_alternatives(self, item: str, limit: int = 5) -> List[Tuple[str, float]]:
        """
        Find similar items based on graph proximity.
        """
        related = self.get_related_nodes(item, depth=2)
        scored = []
        
        for node in related:
            strength = self.edges.get(item, {}).get(node, 0.5)
            scored.append((node, strength))

        # Sort by strength and limit
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:limit]

    def to_json(self):
        """Serialize graph to JSON."""
        return {
            "nodes": self.nodes,
            "edges": self.edges
        }
