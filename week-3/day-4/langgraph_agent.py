"""
Week 3 Day 4: LangGraph Integration
Routing between chat, retrieval, and prediction
"""
import os
import sys
from typing import TypedDict, List, Dict, Optional
from enum import Enum

from langgraph.graph import StateGraph, END

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from day2.predict import predict_match_winner, predict_top_player
from day3.agent import AFLChatAgent, get_team_record, get_player_stats, get_head_to_head

# ============================================================================
# STATE
# ============================================================================

class Intent(str, Enum):
    GREETING = "greeting"
    FACTUAL = "factual"
    PREDICTION = "prediction"
    OFF_TOPIC = "off_topic"
    GOODBYE = "goodbye"

class AFLState(TypedDict):
    user_query: str
    conversation_history: List[Dict[str, str]]
    detected_intent: Optional[str]
    tool_results: Optional[Dict]
    final_response: str
    needs_clarification: bool
    prediction_disclaimer: Optional[str]

# ============================================================================
# NODES
# ============================================================================

def router_node(state: AFLState) -> AFLState:
    """Classify intent and route"""
    query = state["user_query"].lower()
    
    prediction_keywords = ['predict', 'will win', 'who will', 'forecast', 'odds', 'chance']
    off_topic_keywords = ['weather', 'politics', 'cricket', 'movie']
    greeting_keywords = ['hello', 'hi', 'greetings']
    goodbye_keywords = ['bye', 'goodbye', 'see you']
    
    if any(kw in query for kw in off_topic_keywords):
        intent = "off_topic"
    elif any(kw in query for kw in prediction_keywords):
        intent = "prediction"
    elif any(kw in query for kw in greeting_keywords):
        intent = "greeting"
    elif any(kw in query for kw in goodbye_keywords):
        intent = "goodbye"
    else:
        intent = "factual"
    
    return {**state, "detected_intent": intent}

def prediction_node(state: AFLState) -> AFLState:
    """Handle prediction queries"""
    query = state["user_query"]
    
    # Extract teams (simplified)
    teams = ['Collingwood Magpies', 'Carlton Blues', 'Hawthorn Hawks', 'Richmond Tigers']
    found_teams = [t for t in teams if t.lower() in query.lower()]
    
    if len(found_teams) >= 2:
        result = predict_match_winner(found_teams[0], found_teams[1])
        response = f"Prediction: {result['winner']} has {result['probability']:.0%} win probability (confidence: {result['confidence']})"
        disclaimer = "This is a prediction based on historical data, not a certainty."
    else:
        response = "Prediction ke liye do teams ke naam batayein. Jaise: 'Collingwood vs Carlton'"
        disclaimer = None
    
    return {
        **state,
        "final_response": response,
        "prediction_disclaimer": disclaimer,
        "tool_results": {"prediction": result} if len(found_teams) >= 2 else None
    }

def retrieval_node(state: AFLState) -> AFLState:
    """Handle factual queries"""
    agent = AFLChatAgent()
    response = agent.chat(state["user_query"])
    return {**state, "final_response": response}

def refusal_node(state: AFLState) -> AFLState:
    """Handle off-topic queries"""
    response = "Main sirf AFL ki madad kar sakta hoon. Kya aap koi AFL team, player, ya match ke baare mein jaanna chahte hain?"
    return {**state, "final_response": response}

def validation_node(state: AFLState) -> AFLState:
    """Validate results"""
    if state["detected_intent"] == "prediction" and not state.get("tool_results"):
        return {**state, "needs_clarification": True}
    return state

def response_node(state: AFLState) -> AFLState:
    """Format final response"""
    response = state.get("final_response", "")
    if state.get("prediction_disclaimer"):
        response += f"\n\n{state['prediction_disclaimer']}"
    return {**state, "final_response": response}

# ============================================================================
# ROUTING
# ============================================================================

def route_intent(state: AFLState) -> str:
    intent = state.get("detected_intent", "")
    routes = {
        "greeting": "retrieval_node",
        "factual": "retrieval_node",
        "prediction": "prediction_node",
        "off_topic": "refusal_node",
        "goodbye": "retrieval_node",
    }
    return routes.get(intent, "retrieval_node")

# ============================================================================
# GRAPH
# ============================================================================

def build_graph():
    workflow = StateGraph(AFLState)
    
    workflow.add_node("router_node", router_node)
    workflow.add_node("prediction_node", prediction_node)
    workflow.add_node("retrieval_node", retrieval_node)
    workflow.add_node("refusal_node", refusal_node)
    workflow.add_node("validation_node", validation_node)
    workflow.add_node("response_node", response_node)
    
    workflow.set_entry_point("router_node")
    workflow.add_conditional_edges("router_node", route_intent)
    
    for node in ["prediction_node", "retrieval_node", "refusal_node"]:
        workflow.add_edge(node, "validation_node")
    
    workflow.add_edge("validation_node", "response_node")
    workflow.add_edge("response_node", END)
    
    return workflow.compile()

# ============================================================================
# PUBLIC API
# ============================================================================

_graph = None

def get_graph():
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph

def run_agent(query: str, history: List[Dict] = None) -> Dict:
    """Run the agent"""
    graph = get_graph()
    state = {
        "user_query": query,
        "conversation_history": history or [],
        "detected_intent": None,
        "tool_results": None,
        "final_response": "",
        "needs_clarification": False,
        "prediction_disclaimer": None
    }
    result = graph.invoke(state)
    return {
        "response": result.get("final_response", ""),
        "intent": result.get("detected_intent", ""),
        "needs_clarification": result.get("needs_clarification", False)
    }

if __name__ == "__main__":
    print(run_agent("Assalam-o-Alaikum"))
    print(run_agent("Who will win Collingwood vs Carlton?"))
    print(run_agent("What's the weather?"))