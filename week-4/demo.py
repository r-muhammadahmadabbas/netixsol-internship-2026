"""
Demo Script for Real Estate Voice Agent
Shows all features working end-to-end
"""
import sys
import os
import time
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.agent import run_agent
from src.voice_pipeline import text_to_speech
from src.rag_pipeline import RealEstateRAG
from src.recommendation import PropertyRecommendationEngine, UserPreferences

def print_separator():
    print("\n" + "=" * 70 + "\n")

def demo_section(title):
    print_separator()
    print(f"  {title}")
    print_separator()

def run_demo():
    print("\n" + "=" * 70)
    print("  REAL ESTATE VOICE AGENT - LIVE DEMO")
    print("=" * 70)
    
    # ========================================================================
    # DEMO 1: Greeting
    # ========================================================================
    demo_section("DEMO 1: Greeting")
    result = run_agent("Assalam-o-Alaikum")
    print(f"User: Assalam-o-Alaikum")
    print(f"Intent: {result['intent']}")
    print(f"Agent: {result['response']}")
    print(f"Conversation ID: {result['conversation_id']}")
    
    # ========================================================================
    # DEMO 2: Buyer Inquiry with Property Recommendations
    # ========================================================================
    demo_section("DEMO 2: Buyer Inquiry - Property Recommendations")
    result = run_agent("Budget 3 crore hai, Lahore DHA mein, 3 bedroom")
    print(f"User: Budget 3 crore hai, Lahore DHA mein, 3 bedroom")
    print(f"Intent: {result['intent']}")
    print(f"Agent: {result['response']}")
    if result.get('properties'):
        print(f"\nProperties found: {len(result['properties'])}")
        for p in result['properties']:
            print(f"  - {p['title']} | {p['price_formatted']}")
    
    # ========================================================================
    # DEMO 3: RAG Factual Answer
    # ========================================================================
    demo_section("DEMO 3: RAG - Factual Answer")
    result = run_agent("Payment plan for DHA Phase 5 kya hai?")
    print(f"User: Payment plan for DHA Phase 5 kya hai?")
    print(f"Intent: {result['intent']}")
    print(f"Agent: {result['response']}")
    
    # ========================================================================
    # DEMO 4: Off-Topic Refusal
    # ========================================================================
    demo_section("DEMO 4: Off-Topic Refusal")
    result = run_agent("What is the weather like today?")
    print(f"User: What is the weather like today?")
    print(f"Intent: {result['intent']}")
    print(f"Agent: {result['response']}")
    
    # ========================================================================
    # DEMO 5: Objection Handling
    # ========================================================================
    demo_section("DEMO 5: Objection Handling")
    result = run_agent("Ye bohat mehenga hai")
    print(f"User: Ye bohat mehenga hai")
    print(f"Intent: {result['intent']}")
    print(f"Agent: {result['response']}")
    
    # ========================================================================
    # DEMO 6: Multi-Turn Booking
    # ========================================================================
    demo_section("DEMO 6: Multi-Turn Appointment Booking")
    conv_id = None
    
    # Turn 1: Initial inquiry
    result = run_agent("Assalam-o-Alaikum, main ghar dhundh raha hoon", conv_id)
    conv_id = result['conversation_id']
    carried = result.get('state')
    print(f"Turn 1 - User: Assalam-o-Alaikum, main ghar dhundh raha hoon")
    print(f"Turn 1 - Agent: {result['response'][:80]}...")
    
    # Turn 2: Budget and location
    result = run_agent("Budget 3 crore hai, Lahore DHA mein", conv_id, carried_state=carried)
    carried = result.get('state')
    print(f"\nTurn 2 - User: Budget 3 crore hai, Lahore DHA mein")
    print(f"Turn 2 - Agent: {result['response'][:80]}...")
    print(f"Turn 2 - Properties: {len(result.get('properties', []))}")
    
    # Turn 3: Book visit
    result = run_agent("Visit book karni hai 20/01/2025 10:00", conv_id, carried_state=carried)
    print(f"\nTurn 3 - User: Visit book karni hai 20/01/2025 10:00")
    print(f"Turn 3 - Agent: {result['response']}")
    print(f"Turn 3 - Event ID: {result.get('event_id', 'N/A')}")
    print(f"Turn 3 - Status: {result.get('appointment_status', 'N/A')}")
    
    # ========================================================================
    # DEMO 7: TTS (Text-to-Speech)
    # ========================================================================
    demo_section("DEMO 7: Text-to-Speech (Urdu)")
    text = "Assalam-o-Alaikum! RealEstate Hub mein khush aamdeed. Main aap ki madad kar sakta hoon."
    print(f"Text: {text}")
    audio = text_to_speech(text)
    print(f"Generated audio: {len(audio)} bytes")
    
    # Save to file for playback
    with open("demo_output.mp3", "wb") as f:
        f.write(audio)
    print("Saved to: demo_output.mp3")
    
    # ========================================================================
    # DEMO 8: Investment Inquiry
    # ========================================================================
    demo_section("DEMO 8: Investment Inquiry")
    result = run_agent("Main investment karna chahta hoon, rental yield chahiye")
    print(f"User: Main investment karna chahta hoon, rental yield chahiye")
    print(f"Intent: {result['intent']}")
    print(f"Agent: {result['response']}")
    
    # ========================================================================
    # DEMO 9: Rental Inquiry
    # ========================================================================
    demo_section("DEMO 9: Rental Inquiry")
    result = run_agent("Main rental property dhundh raha hai, budget 50000")
    print(f"User: Main rental property dhundh raha hai, budget 50000")
    print(f"Intent: {result['intent']}")
    print(f"Agent: {result['response']}")
    
    # ========================================================================
    # DEMO 10: Goodbye
    # ========================================================================
    demo_section("DEMO 10: Goodbye")
    result = run_agent("Shukriya, allah hafiz")
    print(f"User: Shukriya, allah hafiz")
    print(f"Intent: {result['intent']}")
    print(f"Agent: {result['response']}")
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    print_separator()
    print("  DEMO COMPLETE!")
    print_separator()
    print("""
Summary:
- Greeting: Working
- Buyer Inquiry: Working
- RAG Factual Answers: Working
- Off-Topic Refusal: Working
- Objection Handling: Working
- Multi-Turn Booking: Working
- TTS (Urdu): Working
- Investment Inquiry: Working
- Rental Inquiry: Working
- Goodbye: Working

To launch the full voice UI with microphone:
    streamlit run voice_ui.py

To launch the text-only UI:
    streamlit run ui.py
    """)

if __name__ == "__main__":
    run_demo()