"""
System Health Check - Run this first
Checks all components and reports status
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_component(name, check_func):
    try:
        result = check_func()
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} - {name}")
        return result
    except Exception as e:
        print(f"[ERROR] - {name}: {e}")
        return False

def main():
    print("\n" + "=" * 60)
    print("  SYSTEM HEALTH CHECK")
    print("=" * 60 + "\n")
    
    results = []
    
    # Check 1: Agent
    def check_agent():
        from src.agent import run_agent
        result = run_agent("Assalam-o-Alaikum")
        return result['intent'] == 'greeting'
    results.append(check_component("Agent (LangGraph)", check_agent))
    
    # Check 2: RAG
    def check_rag():
        from src.rag_pipeline import RealEstateRAG
        rag = RealEstateRAG()
        rag.load_data()
        rag.initialize_vector_store()
        results = rag.search("payment plan", top_k=1)
        return len(results) > 0
    results.append(check_component("RAG Pipeline", check_rag))
    
    # Check 3: Recommendation
    def check_recommendation():
        from src.recommendation import PropertyRecommendationEngine, UserPreferences
        engine = PropertyRecommendationEngine()
        prefs = UserPreferences(budget_max=30000000, city="Lahore")
        results = engine.recommend(prefs, top_k=1)
        return len(results) > 0
    results.append(check_component("Recommendation Engine", check_recommendation))
    
    # Check 4: TTS
    def check_tts():
        from src.voice_pipeline import text_to_speech
        audio = text_to_speech("Test")
        return len(audio) > 0
    results.append(check_component("Text-to-Speech (gTTS)", check_tts))
    
    # Check 5: STT
    def check_stt():
        from src.voice_pipeline import is_whisper_available
        return is_whisper_available()
    results.append(check_component("Speech-to-Text (Whisper)", check_stt))
    
    # Check 6: Tools
    def check_tools():
        from src.tools import check_calendar_availability
        result = check_calendar_availability("2025-01-20", "10:00")
        return result.get('available', False)
    results.append(check_component("Calendar Tools", check_tools))
    
    # Check 7: Database
    def check_db():
        from src.tools import init_db
        init_db()
        return os.path.exists("C:/Internship/Netixsol/week-4/real_estate.db")
    results.append(check_component("Database (SQLite)", check_db))
    
    # Summary
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"  RESULTS: {passed}/{total} passed")
    print("=" * 60)
    
    if passed == total:
        print("\n[OK] All systems ready! Run: streamlit run voice_ui.py")
    else:
        print("\n⚠️ Some components need attention.")
        print("Text input will work regardless of STT status.")
    
    print()

if __name__ == "__main__":
    main()