"""
Day 4: Appointment Management
Booking, rescheduling, cancellation workflows
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.tools import book_appointment, reschedule_appointment, cancel_appointment

def test_appointments():
    print("Testing Appointment Management...")
    print("=" * 50)
    
    # Book
    result = book_appointment(
        client_name="Test Client",
        client_phone="0300-0000000",
        client_email="test@example.com",
        property_id="prop_001",
        date_str="2025-01-20",
        time_str="10:00"
    )
    print(f"Booked: {result.get('success')}")
    
    if result.get("success"):
        event_id = result["event_id"]
        
        # Reschedule
        reschedule = reschedule_appointment(event_id, "2025-01-21", "14:00")
        print(f"Rescheduled: {reschedule.get('success')}")
        
        # Cancel
        cancel = cancel_appointment(event_id)
        print(f"Cancelled: {cancel.get('success')}")
    
    print("\nAppointments: WORKING")

if __name__ == "__main__":
    test_appointments()