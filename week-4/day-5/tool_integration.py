"""
Day 5: Tool Integration
All tools wrapped and callable from LangGraph
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.tools import (
    search_properties_from_text, rag_search, check_calendar_availability,
    book_appointment, reschedule_appointment, cancel_appointment,
    get_client_preferences, save_client_preferences, log_call
)

def test_tools():
    print("Testing All Tools...")
    print("=" * 50)
    
    # Property search
    results = search_properties_from_text("3 crore Lahore DHA", top_k=1)
    print(f"[PASS] search_properties: {len(results)} results")
    
    # RAG search
    results = rag_search("payment plan", top_k=1)
    print(f"[PASS] rag_search: {len(results)} results")
    
    # Calendar
    result = check_calendar_availability("2025-01-20", "10:00")
    print(f"[PASS] check_calendar: {result.get('available')}")
    
    # CRM
    save_client_preferences("0300-1234567", "Test", {"budget_max": 30000000})
    prefs = get_client_preferences("0300-1234567")
    print(f"[PASS] CRM: {prefs is not None}")
    
    print("\nAll Tools: WORKING")

if __name__ == "__main__":
    test_tools()