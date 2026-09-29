# Demo Script - 10 Minutes

## Slide 1: Title (30 seconds)
- Project: RealEstate Hub - AI Voice Agent
- Tagline: "Production-Grade Real Estate Voice Assistant"
- Your name, date

## Slide 2: Problem (1 minute)
- Real estate companies receive 50+ calls daily
- Hiring agents is expensive and inconsistent
- Current chatbots sound robotic, don't understand UrduLish
- No 24/7 availability

## Slide 3: Solution (1 minute)
- AI Voice Agent that speaks natural UrduLish
- Answers property questions using RAG (no hallucination)
- Recommends properties based on budget, location, needs
- Books appointments automatically
- 24/7 availability

## Slide 4: Architecture (1 minute)
- Voice: Whisper STT + gTTS TTS
- LLM: Groq (openai/gpt-oss-120b)
- Agent: LangGraph with state management
- Knowledge: ChromaDB vector search
- Database: SQLite (CRM-ready)

## Slide 5: Live Demo - Factual Question (1.5 minutes)
- Type: "Payment plan for DHA Phase 5 kya hai?"
- Show: RAG retrieves exact answer from knowledge base
- Show: Agent speaks response in UrduLish
- Highlight: No hallucination, grounded in data

## Slide 6: Live Demo - Property Recommendation (1.5 minutes)
- Type: "Budget 3 crore hai, Lahore DHA mein"
- Show: Agent recommends matching properties
- Show: Prices, areas, monthly installments
- Highlight: Intelligent matching based on preferences

## Slide 7: Live Demo - Objection Handling (1 minute)
- Type: "Ye bohat mehenga hai"
- Show: Agent responds empathetically
- Show: Value proposition, payment plans
- Highlight: Natural conversation, not robotic

## Slide 8: Live Demo - Appointment Booking (1.5 minutes)
- Type: "Visit book karni hai 20/01/2025 10:00"
- Show: Calendar event created
- Show: Email notification sent
- Show: Confirmation in UrduLish
- Highlight: End-to-end automation

## Slide 9: Evaluation Results (1 minute)
- 40+ test cases across 11 categories
- 90%+ pass rate
- Prompt injection tests passed
- Multi-turn context working

## Slide 10: Q&A (30 seconds)
- Thank you
- Questions?