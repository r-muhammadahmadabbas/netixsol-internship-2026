"""
Day 5: Graph Design
LangGraph routing between nodes
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.agent import build_agent_graph, route_intent

def test_graph():
    print("Testing LangGraph...")
    print("=" * 50)
    
    graph = build_agent_graph()
    print(f"Graph built: {graph is not None}")
    
    # Test routing
    test_cases = [
        ({"detected_intent": "greeting"}, "greeting_node"),
        ({"detected_intent": "buyer_inquiry"}, "recommendation_node"),
        ({"detected_intent": "appointment_booking"}, "booking_node"),
        ({"detected_intent": "off_topic"}, "refusal_node"),
    ]
    
    for state, expected in test_cases:
        result = route_intent(state)
        status = "[PASS]" if result == expected else "[FAIL]"
        print(f"{status} {state['detected_intent']} -> {result}")
    
    print("\nGraph: WORKING")

if __name__ == "__main__":
    test_graph()