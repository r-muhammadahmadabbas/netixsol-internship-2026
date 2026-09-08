# Week 2 — Day 2: LangChain — Tools, Chains, Memory & Your First Framework Agent

## Status: ✅ COMPLETE

## What We'll Do Today

Rebuild yesterday's raw-Python agent using LangChain, and extend it with:
- Real prompt chaining via LCEL (LangChain Expression Language)
- Multiple tools including one hitting a real data source
- Conversation memory for multi-turn dialogues
- Structured output (Pydantic/JSON) and error handling

Goal: Understand what LangChain automates vs. where it adds hidden complexity.

---

## Task Overview

| Task | Description | Status |
|------|-------------|--------|
| 1 | LangChain Setup & Core Concepts (LLM wrapper, Tool, AgentExecutor, Memory mapping; LCEL pipe syntax) | ✅ |
| 2 | Define & Register Tools (@tool decorator, 3+ tools, one real data source, docstrings as prompt) | ✅ |
| 3 | Build Agent with create_tool_calling_agent + AgentExecutor (verbose trace, annotate Reason/Act/Observe) | ✅ |
| 4 | Add Memory (ConversationBufferMemory / RunnableWithMessageHistory, 3-turn conversation test) | ✅ |
| 5 | Structured Output & Error Handling (Pydantic output, tool failure recovery, comparison write-up) | ✅ |

---

## Key Concepts to Learn

### LangChain ↔ Raw Python Mapping

| Raw Python (Day 1) | LangChain Equivalent |
|--------------------|----------------------|
| `Anthropic client` | `ChatAnthropic` (LLM wrapper) |
| Tool JSON schema | `@tool` decorator / `Tool` class |
| `while` loop + `messages` list | `create_tool_calling_agent` + `AgentExecutor` |
| `max_iterations` safeguard | `AgentExecutor(max_iterations=...)` |
| Manual `tool_result` append | Handled internally by AgentExecutor |
| Working memory (Python dict) | `ConversationBufferMemory` / `RunnableWithMessageHistory` |
| Custom logging | `verbose=True` on AgentExecutor |

### LCEL (LangChain Expression Language)
- **Pipe syntax (`|`)**: Composes runnables — each step's output becomes next step's input
- Under the hood: creates a `RunnableSequence` that handles streaming, async, batch, retries automatically
- Replaces old `LLMChain`, `SequentialChain` with a unified, composable interface

---

## Tools Planned

1. **calculator** — Reused from Day 1 (add/subtract)
2. **get_weather** — Reused from Day 1 (stub)
3. **product_lookup** — **NEW**: Reads from local CSV/JSON "database" of products with prices

---

## Deliverables

- `day2-soln.ipynb` — Complete Jupyter notebook with working LangChain agent
- `day2-writeup.md` / `day2-writeup.pdf` — 1-page comparison: raw-Python vs LangChain, annotated trace
- `notes.md` — Daily concepts log (maintained alongside tasks)

---

## Prerequisites

- Day 1 agent working (raw Python)
- `pip install langchain langchain-anthropic langchain-core`
- Anthropic API key set as `ANTHROPIC_API_KEY` environment variable