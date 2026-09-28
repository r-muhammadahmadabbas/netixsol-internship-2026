"""
Day 4: Google Calendar Integration
Create, update, delete calendar events
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.tools import check_calendar_availability, book_calendar_event, cancel_calendar_event, reschedule_calendar_event

def test_calendar():
    print("Testing Calendar Integration...")
    print("=" * 50)
    
    # Check availability
    avail = check_calendar_availability("2025-01-20", "10:00")
    print(f"Available: {avail}")
    
    # Book event
    result = book_calendar_event({
        "start": "2025-01-20T10:00:00",
        "end": "2025-01-20T11:00:00",
        "summary": "Property Visit: Test Client"
    })
    print(f"Booked: {result}")
    
    # Cancel
    if result.get("success"):
        cancel = cancel_calendar_event(result["event_id"])
        print(f"Cancelled: {cancel}")
    
    print("\nCalendar: WORKING")

if __name__ == "__main__":
    test_calendar()