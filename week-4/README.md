# RealEstate Hub - AI Voice Agent

## Overview
Production-ready AI voice agent for real estate companies. Speaks natural UrduLish, answers property questions using RAG, recommends properties, and books appointments automatically.

## Features
- **Voice Input/Output**: Whisper STT + gTTS TTS (UrduLish)
- **Natural Conversations**: Groq LLM (openai/gpt-oss-120b)
- **RAG Knowledge Base**: ChromaDB vector search (no hallucination)
- **Property Recommendations**: Budget, location, amenities matching
- **Appointment Booking**: Calendar + email automation
- **CRM Logging**: SQLite database (call logs, preferences, appointments)
- **LangGraph Orchestration**: State management, intent routing, validation

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys
Create `.env` file:
```
GROQ_API_KEY=gsk_your_key_here
DEEPGRAM_API_KEY=your_key_here
```

### 3. Run the App
```bash
# Voice UI (recommended)
streamlit run voice_ui.py

# Text-only UI
streamlit run ui.py

# API server
uvicorn api:app --reload
```

### 4. Test
```bash
python health_check.py
python demo.py
python evaluation.py
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info |
| `/health` | GET | Health check |
| `/chat` | POST | Send message, get response |
| `/search` | POST | Search properties |
| `/rag` | POST | Search knowledge base |
| `/book` | POST | Book appointment |
| `/voice/tts` | POST | Text to speech |
| `/voice/stt` | POST | Speech to text |

## Project Structure
```
week-4/
├── src/
│   ├── agent.py              # LangGraph agent
│   ├── rag_pipeline.py       # RAG pipeline
│   ├── recommendation.py     # Property recommendations
│   ├── tools.py              # Calendar, email, CRM tools
│   └── voice_pipeline.py     # STT + TTS
├── data/
│   ├── properties.csv        # Property database
│   └── faqs.csv              # FAQ knowledge base
├── api.py                    # FastAPI backend
├── voice_ui.py               # Streamlit voice UI
├── ui.py                     # Streamlit text UI
├── demo.py                   # Demo script
├── evaluation.py             # Evaluation suite
├── health_check.py           # System health check
├── monitoring_plan.md        # Monitoring checklist
├── demo_script.md            # 10-minute demo script
├── requirements.txt          # Dependencies
├── Dockerfile                # Docker setup
└── docker-compose.yml        # Docker compose
```

## Technology Stack
- **LLM**: Groq (openai/gpt-oss-120b) - free tier
- **STT**: Whisper (local) + Deepgram (API)
- **TTS**: gTTS (Google, free)
- **Vector DB**: ChromaDB (local)
- **Database**: SQLite (CRM-ready)
- **Agent**: LangGraph
- **Backend**: FastAPI
- **UI**: Streamlit

## Evaluation
- 40+ test cases across 11 categories
- Categories: buyer, rental, commercial, investment, booking, reschedule, cancellation, off-topic, prompt injection, objection, multi-turn
- Run: `python evaluation.py`

## Monitoring
See `monitoring_plan.md` for:
- Metrics and alert thresholds
- Weekly maintenance schedule
- Retraining loop
- Backup strategy
- Security review cadence

## Demo
See `demo_script.md` for 10-minute stakeholder presentation.

## License
MIT