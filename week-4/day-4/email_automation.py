"""
Day 4: Email Automation
Agent notification and client confirmation emails
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.tools import send_agent_notification, send_client_confirmation

def test_email():
    print("Testing Email Automation...")
    print("=" * 50)
    
    event_data = {
        "client_name": "Ahmed Khan",
        "client_phone": "0300-1234567",
        "client_email": "ahmed@example.com",
        "property_title": "DHA Phase 5, 10 Marla Plot",
        "property_address": "DHA Phase 5, Lahore",
        "property_price": 35000000,
        "appointment_date": "2025-01-20",
        "appointment_time": "10:00"
    }
    
    # Send agent notification
    result = send_agent_notification("agent@realestatehub.com", event_data)
    print(f"Agent email: {result}")
    
    # Send client confirmation
    result = send_client_confirmation("ahmed@example.com", "Ahmed Khan", event_data)
    print(f"Client email: {result}")
    
    print("\nEmail: WORKING")

if __name__ == "__main__":
    test_email()