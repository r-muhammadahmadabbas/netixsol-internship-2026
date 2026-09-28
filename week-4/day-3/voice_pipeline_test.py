"""
Day 3: Voice Pipeline
Speech-to-Text + Text-to-Speech with latency optimization
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.voice_pipeline import text_to_speech, transcribe_audio, is_whisper_available

LATENCY_BUDGET = {
    "stt": {"target": "200-400ms", "provider": "Whisper/Deepgram"},
    "llm": {"target": "500-800ms", "provider": "Groq"},
    "tts": {"target": "200-400ms", "provider": "gTTS"},
    "network": {"target": "100-200ms", "provider": "Edge"},
    "total": {"target": "< 2s", "provider": "End-to-end"}
}

def test_voice_pipeline():
    print("Testing Voice Pipeline...")
    print("=" * 50)
    
    print(f"Whisper available: {is_whisper_available()}")
    
    text = "Assalam-o-Alaikum! RealEstate Hub mein khush aamdeed."
    audio = text_to_speech(text)
    print(f"TTS generated: {len(audio)} bytes")
    
    print("\nLatency Budget:")
    for component, details in LATENCY_BUDGET.items():
        print(f"  {component}: {details['target']} ({details['provider']})")
    
    print("\nVoice Pipeline: WORKING")

if __name__ == "__main__":
    test_voice_pipeline()