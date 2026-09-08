# Week 2 — Day 1: Agent Foundations

## Status: ✅ COMPLETE

## What We Did Today

Built a minimal AI agent from scratch in raw Python using the Anthropic API — no LangChain, no LangGraph. Understood what makes something "agentic" and built the ReAct loop manually.

| Task | Description | Status |
|------|-------------|--------|
| 1 | Agent Concepts & Mental Model (agent vs chatbot vs workflow, ReAct pattern) | ✅ |
| 2 | Tool Calling Fundamentals (JSON schemas, Anthropic tool use) | ✅ |
| 3 | Build a Minimal Agent Loop (while-loop, tool execution, max_iterations) | ✅ |
| 4 | Memory & State Handling (conversation memory vs working memory, logging) | ✅ |
| 5 | Failure Modes & Guardrails (deliberately break agent, list mitigations) | ✅ |

## Key Concepts

### Agent vs Chatbot vs Workflow
- **Chatbot**: One request, one response. No action.
- **Workflow**: Deterministic steps. No LLM reasoning.
- **Agent**: LLM that decides what to do, uses tools, loops until done.

### ReAct Pattern
Reason → Act → Observe → Repeat

The agent loops until the model returns text-only (no more tool calls needed).

### Tool Calling
- Define tools with `name`, `description`, `input_schema` (JSON)
- Model chooses which tool to call based on descriptions
- Execute tool yourself, return result as `tool_result` block
- Repeat the loop

### Agent Loop
```python
while response has tool_use blocks:
    execute tool
    append tool_result to messages
    send messages back to model
    check max_iterations
```

### Memory
- **Conversation memory**: Full message history (passed to every API call)
- **Working memory**: Python variables tracking state (not visible to LLM)

## Tools Defined

1. **calculator** — Adds/subtracts two numbers (for math tasks)
2. **get_weather** — Returns weather for a city (stub/lookup)
3. **read_file** — Reads content of a text file

## Deliverables

- `week-2-day-1-soln.ipynb` — Complete notebook with all 5 tasks
- `task-statement.txt` — Task instructions
- `notes.md` — Prerequisite concepts (ReAct, tool calling, memory)
- `requirements.txt` — Pinned library versions

## Final Code Structure

```python
# Agent loop core
while True:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=messages,
        tools=tools,
        tool_choice={"type": "auto"}
    )
    
    # Check if model wants to use tools
    tool_blocks = [b for b in response.content if b.type == "tool_use"]
    
    if not tool_blocks:
        # Model returned final text answer
        break
    
    # Execute each tool and build tool_result blocks
    tool_results = []
    for block in tool_blocks:
        result = execute_tool(block.name, block.input)
        tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": result})
    
    # Append tool results to conversation
    messages.append({"role": "assistant", "content": response.content})
    messages.append({"role": "user", "content": tool_results})
    
    iteration += 1
    if iteration >= MAX_ITERATIONS:
        break
```

## Key Learnings

1. Tool descriptions directly affect which tool the model calls — be specific
2. The agent loop is deceptively simple — a while loop with a message list
3. Without max_iterations, an ambiguous task causes infinite loops
4. Logging each step is essential for debugging (Task 4)
5. Frameworks like LangChain handle edge cases you haven't thought of yet

## Primary API
Anthropic API via `anthropic==1.4.0`

## Prerequisites from Week 1
- Jupyter notebook usage
- Python basics (functions, lists, dictionaries, while loops)
- JSON schema understanding (from Day 3 feature selection)

## Task 2: Tool Calling Fundamentals (Notes for notes.md)

---

### 1. What Is Tool Calling (Function Calling)?

**Tool calling** lets an LLM request execution of external functions by emitting structured `tool_use` blocks. You (the developer) define the tools, the LLM decides *which* to call and *with what arguments*, you execute them, and return results as `tool_result` blocks. This is the bridge between the LLM's reasoning and the real world.

---

### 2. Anatomy of a Tool Definition (Anthropic API)

Each tool requires **three properties**:

| Property | Purpose | Example |
|----------|---------|---------|
| `name` | Unique identifier (string) | `"calculator"` |
| `description` | Human-readable explanation — **the LLM reads this to decide when to call the tool** | `"Adds two numbers. Use for math questions."` |
| `input_schema` | JSON Schema describing the arguments the tool accepts | `{"type": "object", "properties": {"a": {"type": "number"}, "b": {"type": "number"}}, "required": ["a", "b"]}` |

---

### 3. Three Example Tools with JSON Schemas

#### Tool 1: Calculator (Add/Subtract)
```json
{
  "name": "calculator",
  "description": "Performs basic arithmetic (add, subtract) on two numbers. Use when the user asks for math calculations.",
  "input_schema": {
    "type": "object",
    "properties": {
      "operation": {"type": "string", "enum": ["add", "subtract"], "description": "The operation to perform"},
      "a": {"type": "number", "description": "First operand"},
      "b": {"type": "number", "description": "Second operand"}
    },
    "required": ["operation", "a", "b"]
  }
}
```

#### Tool 2: Weather Lookup (Stub)
```json
{
  "name": "get_weather",
  "description": "Returns current temperature for a given city. Use when the user asks about weather. This is a stub - returns fake data.",
  "input_schema": {
    "type": "object",
    "properties": {
      "city": {"type": "string", "description": "City name (e.g., 'Tokyo', 'New York')"}
    },
    "required": ["city"]
  }
}
```

#### Tool 3: File Reader
```json
{
  "name": "read_file",
  "description": "Reads the content of a text file from the local filesystem. Use when the user asks to read a file.",
  "input_schema": {
    "type": "object",
    "properties": {
      "path": {"type": "string", "description": "Relative or absolute path to the file"}
    },
    "required": ["path"]
  }
}
```

---

### 4. Why Tool Descriptions Matter (Critical)

The `description` is **the only signal** the LLM has about what a tool does and *when* to use it.

| Description Quality | Example | Result |
|---------------------|---------|--------|
| ❌ **Vague** | `"A math tool"` | LLM calls it for "What's 2+2?" but also for "Calculate the derivative" (wrong tool) |
| ❌ **Missing context** | `"Adds numbers"` | LLM doesn't know it handles subtraction too |
| ✅ **Specific + usage hint** | `"Performs basic arithmetic (add, subtract) on two numbers. Use when the user asks for math calculations."` | LLM correctly chooses it for "What's 15 + 27?" and "Subtract 5 from 20" |

**Rule**: Write descriptions as if explaining to a junior developer — include *what it does*, *what it doesn't do*, and *when to use it*.

---

### 5. The Tool Calling Flow (Single Request → Manual Execution → Return Result)

#### Step 1: Send Request with Tools
```python
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": "What's 15 + 27?"}],
    tools=[calculator_tool, weather_tool],
    tool_choice={"type": "auto"}  # Let model decide
)
```

#### Step 2: Model Responds with `tool_use` Block
```json
{
  "type": "tool_use",
  "id": "toolu_01AbCdEfGh...",
  "name": "calculator",
  "input": {"operation": "add", "a": 15, "b": 27}
}
```

#### Step 3: YOU Execute the Tool (Python Function)
```python
def execute_calculator(operation, a, b):
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    raise ValueError(f"Unknown operation: {operation}")

result = execute_calculator("add", 15, 27)  # Returns 42
```

#### Step 4: Return Result as `tool_result` Block
```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_01AbCdEfGh...",
  "content": "Result: 15 + 27 = 42"
}
```

#### Step 5: Append to Conversation & Send Back
```python
messages.append({"role": "assistant", "content": response.content})
messages.append({"role": "user", "content": [tool_result_block]})
```

---

### 6. Key Takeaways for Task 2

1. **Tools = JSON Schemas** — `name`, `description`, `input_schema`. The description is the most important part for reliability.
2. **LLM decides, you execute** — The model outputs `tool_use` blocks; your Python code runs the actual function.
3. **Round-trip** — You append `tool_result` blocks to the conversation and send back to get the final answer.
4. **Stub tools are fine** — For learning, fake implementations (like the weather stub) work perfectly.
5. **This is the atomic unit** — The agent loop (Task 3) is just this flow in a `while` loop.