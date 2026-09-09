# Week 2 — Day 3: LangGraph — Stateful, Multi-Step & Cyclical Agent Workflows

## Status: 🔄 IN PROGRESS

## General Perspective

Yesterday (Day 2) you built agents using LangChain's `create_agent` — a single
loop that runs tools and returns. Today you learn **LangGraph**, which replaces
that flat loop with a **graph** — nodes are steps, edges are transitions, and
the agent can **branch, loop back, and pause** for human input.

This is how real production agents work: they don't just "run tools and answer".
They plan, execute, critique themselves, revise, ask for approval, and remember
what happened across sessions.

---

## What Today's Tasks Cover

### Task 1: Graph Concepts & State Design (Theory First)
**What**: Learn the building blocks before writing any code.
- **StateGraph** — the container that holds your workflow
- **Nodes** — individual steps (functions that do work)
- **Edges** — transitions between nodes (which step comes next)
- **Conditional Edges** — "if X, go here; if Y, go there"
- **State** — a shared dictionary/typed object that every node reads from and writes to

**Why**: You need to think about your workflow as a graph BEFORE coding. Drawing
the diagram first forces you to understand the flow.

**Deliverable**: A State schema + ASCII/Mermaid diagram of your chosen workflow.

---

### Task 2: Build a Linear Graph (Your First LangGraph)
**What**: Build the simplest possible graph — 3-4 nodes in a straight line.
Example: `plan → retrieve → generate → format`

**Key learning**: Each node is a function. The graph calls them in order. State
flows between them. You print state after each node to see it update.

**Day 2 connection**: You can reuse your `@tool` functions inside nodes.

**Deliverable**: A working linear graph that runs end-to-end.

---

### Task 3: Add Conditional Edges & Cycles (The Real Power)
**What**: Add a "critique" node that decides: is the output good enough?
- YES → go to finish
- NO → go back to "generate" and try again

This is a **self-correction loop** — the agent fixes its own mistakes.

**Key learning**: This loop is trivial in LangGraph but painful in AgentExecutor.
You also add a `max_retries` counter to prevent infinite loops.

**Deliverable**: A graph with a conditional loop + retry limit.

---

### Task 4: Human-in-the-Loop & Interrupts (Production Pattern)
**What**: Add a pause where the graph stops and waits for human approval
before doing something risky (e.g., "send email" or "place order").

**Key learning**: LangGraph can `interrupt_before` or `interrupt_after` any node.
You resume the graph after the human says yes/no.

**Discussion**: When does a real product need human approval vs. full autonomy?

**Deliverable**: A graph that pauses, waits, and resumes.

---

### Task 5: Persistence & Debugging (Production Readiness)
**What**: Add a checkpointer (`MemorySaver`) so state survives across runs.
Demonstrate resuming a paused conversation and replaying/debugging past runs.

**Key comparison**: When to use LangChain AgentExecutor vs. LangGraph in
real projects.

**Deliverable**: Persisted graph + state history/replay demo + comparison write-up.

---

## How Today Differs from Day 2

| Day 2 (AgentExecutor) | Day 3 (LangGraph) |
|------------------------|-------------------|
| Single loop: tools → answer | Graph: nodes + edges + conditions |
| No branching | Conditional routing |
| No self-correction | Agent can critique and retry |
| No human approval | Interrupts for human-in-the-loop |
| State lost after run | Checkpointer persists state |
| Hard to visualize flow | Graph is explicit and visual |

---

## Prerequisites
- Day 2 agent working (LangChain + tools + memory)
- `pip install langgraph langchain-core`
- Groq API key (`GROQ_API_KEY`)

---

## Deliverables
- `day3-soln.ipynb` — Complete Jupyter notebook
- `notes.md` — Daily concepts log
- Graph diagram (Mermaid or ASCII in notebook)
