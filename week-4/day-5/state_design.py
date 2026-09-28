"""
Day 5: LangGraph State Design
Complete state schema for the agent
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.agent import AgentState, create_initial_state

def test_state():
    print("Testing LangGraph State...")
    print("=" * 50)
    
    state = create_initial_state()
    
    print(f"Conversation ID: {state['conversation_id']}")
    print(f"Current turn: {state['current_turn']}")
    print(f"Max retries: {state['max_retries']}")
    print(f"History length: {len(state['conversation_history'])}")
    
    # Add a message
    state["conversation_history"].append({"role": "user", "content": "Test"})
    state["current_turn"] = 1
    
    print(f"After message - turn: {state['current_turn']}")
    print(f"History length: {len(state['conversation_history'])}")
    
    print("\nState: WORKING")

if __name__ == "__main__":
    test_state()