"""
Day 1: Conversation Flows
7 complete conversation flow designs
"""

FLOWS = {
    "buyer_inquiry": [
        "Greeting",
        "Needs Assessment (budget, area, bedrooms)",
        "Property Recommendations",
        "Objection Handling",
        "Schedule Visit",
        "Confirm Details",
        "Email/Calendar",
        "Goodbye"
    ],
    "rental_inquiry": [
        "Greeting",
        "Needs (budget, area, furnished?)",
        "Available Units",
        "Compare Options",
        "Schedule Viewing",
        "Confirm",
        "Goodbye"
    ],
    "commercial_inquiry": [
        "Greeting",
        "Business Type",
        "Size/Location Needs",
        "Commercial Options",
        "ROI Discussion",
        "Schedule Site Visit",
        "Assign Specialist",
        "Goodbye"
    ],
    "investment_inquiry": [
        "Greeting",
        "Investment Goals (yield, appreciation)",
        "Investment Options",
        "ROI Projection",
        "Risk Discussion",
        "Schedule Meeting",
        "Goodbye"
    ],
    "returning_customer": [
        "Greeting (personalized)",
        "Recap Last Interaction",
        "Update Preferences",
        "New Recommendations",
        "Next Steps",
        "Goodbye"
    ],
    "appointment_reschedule": [
        "Greeting",
        "Identify Appointment",
        "Check Availability",
        "Propose New Times",
        "Confirm",
        "Update Calendar",
        "Notify Employee",
        "Goodbye"
    ],
    "appointment_cancellation": [
        "Greeting",
        "Identify Appointment",
        "Confirm Cancellation",
        "Update Calendar",
        "Notify Employee",
        "Offer Rebooking",
        "Goodbye"
    ]
}

if __name__ == "__main__":
    for flow_name, steps in FLOWS.items():
        print(f"\n{flow_name.upper()}:")
        for i, step in enumerate(steps, 1):
            print(f"  {i}. {step}")