# Week 2 Day 1: Agent Foundations — Write-up

## ReAct Loop

The **ReAct (Reason → Act → Observe)** pattern is the core cognitive loop powering every LLM agent. Unlike a chatbot (single request/response) or workflow (deterministic steps), an agent autonomously decides its next action based on observations from tool executions.

### Loop Pseudocode
```python
while iteration < MAX_ITERATIONS:
    response = client.messages.create(messages=messages, tools=tools, ...)
    tool_blocks = [b for b in response.content if b.type == "tool_use"]
    
    if not tool_blocks:           # Text-only → final answer
        break
    
    for block in tool_blocks:     # Execute each tool
        result = execute_tool(block.name, block.input)
        tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": result})
    
    messages.append({"role": "assistant", "content": response.content})
    messages.append({"role": "user", "content": tool_results})
    iteration += 1
```

### Example: "Compare weather in Tokyo and Paris"
| Iteration | Reason | Act | Observe |
|-----------|--------|-----|---------|
| 1 | Need both cities' weather | `get_weather("Tokyo")` | Tokyo: 22°C |
| 2 | Have Tokyo, need Paris | `get_weather("Paris")` | Paris: 18°C |
| 3 | Compare: 22 > 18 | — | **Final: "Tokyo is warmer"** |

**Key safeguard**: `MAX_ITERATIONS` (default 8–10) prevents infinite loops on ambiguous tasks.

---

## Tool Schemas Used

Three tools defined with Anthropic's tool-use format (name, description, input_schema):

### 1. Calculator
```json
{
  "name": "calculator",
  "description": "Performs basic arithmetic (add, subtract) on two numbers. Use when the user asks for math calculations.",
  "input_schema": {
    "type": "object",
    "properties": {
      "operation": {"type": "string", "enum": ["add", "subtract"]},
      "a": {"type": "number"}, "b": {"type": "number"}
    },
    "required": ["operation", "a", "b"]
  }
}
```

### 2. Weather Lookup (Stub)
```json
{
  "name": "get_weather",
  "description": "Returns current temperature for a given city. Use when the user asks about weather.",
  "input_schema": {
    "type": "object",
    "properties": {"city": {"type": "string"}},
    "required": ["city"]
  }
}
```

### 3. File Reader
```json
{
  "name": "read_file",
  "description": "Reads content of a text file from the local filesystem.",
  "input_schema": {
    "type": "object",
    "properties": {"path": {"type": "string"}},
    "required": ["path"]
  }
}
```

**Critical insight**: The `description` field is the *only* signal the LLM has for tool selection. Vague descriptions ("A math tool") cause misfires; specific ones ("Performs add/subtract. Use for math calculations") enable reliable routing.

---

## Failure Modes Observed & Mitigations

| # | Failure Mode | Trigger | Mitigation Implemented |
|---|--------------|---------|------------------------|
| 1 | **Infinite loops** | Ambiguous request ("Figure it out") | Hard `max_iterations=8`; graceful exit with failure summary |
| 2 | **Hallucinated tool calls** | Request for undefined tool ("Search the web") | `validate_tool_call()` checks `name ∈ ALLOWED_TOOLS` before execution; returns error as `tool_result` |
| 3 | **Wrong tool arguments** | Unsupported operation ("multiply") | Schema validation rejects invalid enum values & missing required fields |
| 4 | **Silent errors** | Tool returns "Error: unavailable" | `is_error_result()` scans for "Error:", "Failed:", "Exception:"; logs warning, lets LLM decide |
| 5 | **Context overflow** | Many iterations → token limit | (Future) Summarize/truncate history after N turns |

### Test Results
| Test | Query | Outcome |
|------|-------|---------|
| 1 | "What's 15 + 27?" | ✅ 1 iteration, correct answer (42) |
| 2 | "Use broken_calculator to add 10 and 5" | ⚠️ Silent error detected, logged, continued |
| 3 | "Search the web for weather in Tokyo" | 🛡️ Hallucinated tool rejected, error returned to LLM |
| 4 | "Calculate 6 multiplied by 7" | 🛡️ Invalid operation caught by schema validation |
| 5 | "Figure it out" | ⏱️ Max iterations reached, graceful stop |

---

## Why Frameworks Exist (LangGraph, LangChain, CrewAI)

> **Frameworks don't add magic — they add guardrails and structure for the failures documented above.**

- **LangGraph** replaces the `while` loop with a state graph: explicit nodes/edges, conditional routing, built-in `max_iterations`, checkpointing, human-in-the-loop interrupts.
- **LangChain** provides Pydantic-validated tool schemas, automatic retry logic, streaming, token counting, and 100+ integrations (vector stores, SQL, APIs) eliminating boilerplate.
- **CrewAI** adds role-based agents, task delegation, and multi-agent orchestration — beyond a single-loop agent's capability.

**Bottom line**: The raw agent teaches *what* happens under the hood. Frameworks handle *how* to make it reliable at scale. When they break, you now know why.