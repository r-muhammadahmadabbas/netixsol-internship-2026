# Week 4 Day 5 — LangGraph Orchestration & Tool Calling

## Overview
Transform the system into a true AI agent with LangGraph state management and tool orchestration.

## Tasks
1. **LangGraph State Design** — Conversation history, user profile, preferences, budget, intent, tool outputs, appointment status
2. **Graph Design** — Routing between Greeting, Intent Detection, RAG, Recommendation, Booking, Rescheduling, Cancellation, Email, Goodbye
3. **Tool Integration** — Search Property, Calendar, Email, CRM, Availability Checker, RAG Search
4. **Validation** — Never book unavailable slots, never recommend unavailable properties, ask clarification
5. **State Logging** — Log every node transition, annotated execution traces

## Deliverables
- LangGraph state schema
- Full agent graph
- Tool wrappers
- Validation logic
- State logging system

## How to Run
```bash
# Run agent
python agent.py
```