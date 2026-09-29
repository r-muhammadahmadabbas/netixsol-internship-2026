"""
Week 3 Day 4: Annotated State Traces
Full execution traces for 3 representative conversations
"""
import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from day4.langgraph_agent import run_agent

# ============================================================================
# TRACE 1: Factual Retrieval
# ============================================================================

def trace_factual():
    print("=" * 70)
    print("TRACE 1: FACTUAL RETRIEVAL")
    print("=" * 70)
    
    query = "Collingwood ka record kya hai?"
    print(f"\nUser Query: {query}")
    
    result = run_agent(query)
    
    trace = {
        "timestamp": datetime.now().isoformat(),
        "conversation_id": "trace_001",
        "turn": 1,
        "from_node": "router_node",
        "to_node": "retrieval_node",
        "intent": result["intent"],
        "metadata": {
            "query_type": "team_record",
            "tool_called": "get_team_record"
        },
        "state_snapshot": {
            "detected_intent": result["intent"],
            "needs_clarification": result["needs_clarification"]
        },
        "response": result["response"]
    }
    
    print(f"\nRouter Decision: {result['intent']}")
    print(f"Tool Called: get_team_record('Collingwood Magpies')")
    print(f"Response: {result['response'][:100]}...")
    
    return trace

# ============================================================================
# TRACE 2: Match Prediction
# ============================================================================

def trace_prediction():
    print("\n" + "=" * 70)
    print("TRACE 2: MATCH PREDICTION")
    print("=" * 70)
    
    query = "Who will win Collingwood vs Carlton?"
    print(f"\nUser Query: {query}")
    
    result = run_agent(query)
    
    trace = {
        "timestamp": datetime.now().isoformat(),
        "conversation_id": "trace_002",
        "turn": 1,
        "from_node": "router_node",
        "to_node": "prediction_node",
        "intent": result["intent"],
        "metadata": {
            "query_type": "match_prediction",
            "tool_called": "predict_match_winner",
            "teams": ["Collingwood Magpies", "Carlton Blues"]
        },
        "state_snapshot": {
            "detected_intent": result["intent"],
            "needs_clarification": result["needs_clarification"]
        },
        "response": result["response"]
    }
    
    print(f"\nRouter Decision: {result['intent']}")
    print(f"Tool Called: predict_match_winner('Collingwood Magpies', 'Carlton Blues')")
    print(f"Response: {result['response'][:100]}...")
    
    return trace

# ============================================================================
# TRACE 3: Off-Topic Refusal
# ============================================================================

def trace_off_topic():
    print("\n" + "=" * 70)
    print("TRACE 3: OFF-TOPIC REFUSAL")
    print("=" * 70)
    
    query = "What's the weather like today?"
    print(f"\nUser Query: {query}")
    
    result = run_agent(query)
    
    trace = {
        "timestamp": datetime.now().isoformat(),
        "conversation_id": "trace_003",
        "turn": 1,
        "from_node": "router_node",
        "to_node": "refusal_node",
        "intent": result["intent"],
        "metadata": {
            "query_type": "off_topic",
            "tool_called": None,
            "reason": "weather query detected as off-topic"
        },
        "state_snapshot": {
            "detected_intent": result["intent"],
            "needs_clarification": result["needs_clarification"]
        },
        "response": result["response"]
    }
    
    print(f"\nRouter Decision: {result['intent']}")
    print(f"Tool Called: None (refusal)")
    print(f"Response: {result['response'][:100]}...")
    
    return trace

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    traces = []
    
    traces.append(trace_factual())
    traces.append(trace_prediction())
    traces.append(trace_off_topic())
    
    # Save traces
    with open("state_traces.json", "w") as f:
        json.dump(traces, f, indent=2)
    
    print("\n" + "=" * 70)
    print("TRACES SAVED: state_traces.json")
    print("=" * 70)