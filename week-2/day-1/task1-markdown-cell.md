# Task 1: Agent Concepts & Mental Model

## 1. Agent vs Chatbot vs Workflow

### **Chatbot**
- **Definition**: A conversational interface that responds to user input with a single response.
- **Flow**: One request → One response.
- **Capabilities**: No tools, no autonomy, no memory beyond the current session context.
- **Example**: Basic ChatGPT interface, FAQ customer service bot.
- **Key Characteristic**: **Passive** — waits for input, gives output, does not act on the world.

### **Workflow**
- **Definition**: A predefined, deterministic sequence of steps that always executes the same way.
- **Flow**: Fixed path — every branch is known before execution.
- **Capabilities**: No LLM reasoning involved; purely programmatic logic (if/else, loops, function calls).
- **Example**: "If temperature > 100°C → send alert email; else → log reading."
- **Key Characteristic**: **Rigid** — the computer follows instructions; no decision-making by an LLM.

### **Agent**
- **Definition**: An LLM that **decides what to do next** based on observations from the world.
- **Flow**: Continuous loop — Reason → Act → Observe → Repeat until task completion.
- **Capabilities**:
  - **Autonomy**: Chooses its own actions based on context.
  - **Tool Use**: Invokes external functions (APIs, databases, file I/O, calculations).
  - **Multi-step Planning**: Breaks complex tasks into smaller steps, solves each, combines results.
  - **Self-Correction**: If a tool fails or returns unexpected results, it can retry with a different approach.
- **Example**: An agent that looks up weather in two cities, compares temperatures, and answers "Which is warmer?"
- **Key Characteristic**: **Active** — decides, acts, observes, decides again.

---

## 2. What Makes Something "Agentic"? (The Four Pillars)

| Trait | What It Means | Why It Matters |
|-------|---------------|----------------|
| **Autonomy** | The model decides the next step based on prior observations, not a one-shot prompt. | Handles tasks it wasn't explicitly programmed for; adapts to novel situations. |
| **Tool Use** | The model invokes external functions to get information it doesn't have internally. | Accesses real-time data, performs calculations, reads/writes files, calls APIs. |
| **Multi-step Planning** | Breaks a complex task into smaller steps, executes each, and synthesizes results. | Solves problems too complex for a single LLM call (e.g., research + analysis + report). |
| **Self-Correction** | Detects failures (tool errors, bad results) and tries alternative approaches. | Reduces failure rates; handles edge cases without human intervention. |

**The Spectrum**: Chatbot (no tools, no loop) ←→ Workflow (deterministic steps) ←→ Full Agent (tools + loop + memory + correction). Most production systems sit somewhere in between.

---

## 3. The ReAct Pattern (Reason → Act → Observe → Repeat)

The **ReAct pattern** is the core cognitive loop that every agent follows. It interleaves **reasoning** (thinking) with **acting** (tool calls) and **observing** (processing results).

### Pseudocode Representation
```python
while task_not_complete:
    # REASON: Think about what to do next
    thought = llm_reason(current_state, available_tools)
    
    # ACT: Execute a tool based on reasoning
    if thought.requires_tool:
        tool_result = execute_tool(thought.tool_name, thought.tool_args)
    
    # OBSERVE: Process the result
    observation = process_result(tool_result)
    current_state.update(observation)
    
    # REPEAT: Loop back to reasoning with new information
```

### Visual Diagram: "Compare Weather in Tokyo vs Paris"

```
USER: "Look up weather in Tokyo and Paris, tell me which is warmer."
                    │
                    ▼
        ┌───────────────────────┐
        │ REASON: "I need       │
        │ weather data for      │
        │ both cities. I'll     │
        │ call the weather tool.│
        └───────────┬───────────┘
                    ▼
        ┌───────────────────────┐
        │ ACT: Call             │
        │ weather_tool("Tokyo") │
        └───────────┬───────────┘
                    ▼
        ┌───────────────────────┐
        │ OBSERVE: Tokyo = 22°C │
        └───────────┬───────────┘
                    ▼
        ┌───────────────────────┐
        │ REASON: "Got Tokyo.   │
        │ Now I need Paris."    │
        └───────────┬───────────┘
                    ▼
        ┌───────────────────────┐
        │ ACT: Call             │
        │ weather_tool("Paris") │
        └───────────┬───────────┘
                    ▼
        ┌───────────────────────┐
        │ OBSERVE: Paris = 18°C │
        └───────────┬───────────┘
                    ▼
        ┌───────────────────────┐
        │ REASON: "Tokyo (22°C) │
        │ > Paris (18°C). Task  │
        │ complete."            │
        └───────────┬───────────┘
                    ▼
        FINAL ANSWER: "Tokyo is warmer than Paris (22°C vs 18°C)."
```

**Key Insight**: The loop continues until the LLM returns a **text-only response** (no `tool_use` blocks), signaling the final answer.

---

## 4. When Is an Agent Overkill? (2–3 Sentences)

An agent is **overkill** when:
- The task is **deterministic** and solvable with a simple script or formula (e.g., "Calculate 15% tax on $200" → just write `0.15 * 200`).
- **No external data or tools are needed** — the LLM can answer directly from its training knowledge (e.g., "Summarize this paragraph" → single prompt suffices).
- The problem requires **no multi-step reasoning or decision-making** — a single well-crafted prompt produces the desired output reliably.

**Rule of Thumb**: If you can solve it with **one prompt + zero tool calls + no looping**, don't build an agent. The added complexity (loop logic, error handling, token costs) isn't justified.

---

## 5. Key Takeaways for Task 1

1. **Agent ≠ Chatbot ≠ Workflow** — The defining difference is *who decides the next action*: human (chatbot), programmer (workflow), or LLM (agent).
2. **ReAct is the universal agent loop** — Reason → Act → Observe → Repeat. Every agent framework (LangGraph, CrewAI, etc.) implements this pattern under the hood.
3. **"Agentic" = Autonomy + Tools + Planning + Correction** — Missing any pillar means it's not a full agent.
4. **Judgment matters** — Knowing when *not* to use an agent is as important as knowing how to build one.