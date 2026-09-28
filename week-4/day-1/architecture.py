"""
Day 1: Voice Agent Architecture
Complete pipeline documentation and design
"""

ARCHITECTURE = """
# RealEstate Hub - Voice Agent Architecture

## Pipeline Overview

[Phone Call] -> [Telephony] -> [STT] -> [LangGraph Agent] -> [TTS] -> [Telephony] -> [Phone Call]
                              |              |              |
                         [RAG + SQL]    [Tools]        [Memory]
                              |              |              |
                        [Vector DB]   [Calendar/Email]  [Long-term]

## Components

### 1. Speech-to-Text (STT)
- Whisper (local, free) - primary
- Deepgram (API, free tier) - fallback
- Handles: Urdu, UrduLish, English

### 2. LLM Reasoning
- Groq: openai/gpt-oss-120b (free tier)
- Handles: intent detection, tool calling, memory, personality

### 3. Tool Calling
- search_properties: Find matching properties
- rag_search: Factual Q&A from knowledge base
- check_calendar: Verify availability
- book_appointment: Create calendar event + send email
- reschedule_appointment: Update calendar event
- cancel_appointment: Delete calendar event

### 4. Retrieval (RAG)
- ChromaDB vector store
- Property descriptions, FAQs, brochures
- Hybrid: structured (SQL) + semantic (vector)

### 5. Memory
- Short-term: conversation history (in-state)
- Long-term: user preferences (SQLite)

### 6. Text-to-Speech (TTS)
- gTTS (Google, free)
- Urdu language support

### 7. Telephony
- Web-based (Streamlit) for demo
- Twilio/Vonage for production phone integration

### 8. Workflow Orchestration
- LangGraph state machine
- Intent-based routing
- Validation and fallback handling
"""

print(ARCHITECTURE)