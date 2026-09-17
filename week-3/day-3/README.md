# Week 3 Day 3 — Domain-Scoped AFL Chat Agent

## Overview
Build a conversational AFL assistant that:
- Only discusses AFL topics
- Grounds answers in real data (no hallucinated stats)
- Politely declines off-topic requests

## Tasks
1. Scope Definition & System Prompt Design
2. Build Retrieval Layer (structured + semantic)
3. Wire Retrieval into LangChain
4. Memory & Multi-Turn Conversations
5. Guardrail Evaluation

## Data
- `data/afl_datasets/` — From Day 1
- `features/` — From Day 1-2
- `models/` — From Day 2 (saved pipelines)

## How to Run
```bash
jupyter notebook
```

## Deliverables
- Working LangChain AFL chat agent.
- Guardrail evaluation report (test prompts → pass/fail)
