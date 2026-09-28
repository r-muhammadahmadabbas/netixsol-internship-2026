"""
Day 7: Stakeholder Demonstration
10-minute live demo script
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.agent import run_agent
from src.voice_pipeline import text_to_speech

DEMO_SCRIPT = [
    {"time": "0:00-1:00", "action": "Show greeting", "input": "Assalam-o-Alaikum"},
    {"time": "1:00-2:30", "action": "Property inquiry", "input": "Budget 3 crore hai, Lahore DHA mein"},
    {"time": "2:30-3:30", "action": "RAG factual answer", "input": "Payment plan for DHA Phase 5 kya hai?"},
    {"time": "3:30-4:30", "action": "Objection handling", "input": "Ye bohat mehenga hai"},
    {"time": "4:30-5:30", "action": "Appointment booking", "input": "Visit book karni hai 20/01/2025 10:00"},
    {"time": "5:30-6:30", "action": "Show calendar event", "input": ""},
    {"time": "6:30-7:00", "action": "Show email notification", "input": ""},
    {"time": "7:00-8:30", "action": "Rescheduling", "input": "Appointment reschedule karni hai"},
    {"time": "8:30-9:30", "action": "Cancellation", "input": "Appointment cancel karni hai"},
    {"time": "9:30-10:00", "action": "Q&A", "input": ""},
]

def run_demo():
    print("Stakeholder Demo Script")
    print("=" * 60)
    for step in DEMO_SCRIPT:
        print(f"\n[{step['time']}] {step['action']}")
        if step['input']:
            print(f"  Input: {step['input']}")
            result = run_agent(step['input'])
            print(f"  Response: {result['response'][:80]}...")

if __name__ == "__main__":
    run_demo()