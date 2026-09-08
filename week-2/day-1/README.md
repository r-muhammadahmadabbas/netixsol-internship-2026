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

- `day1-soln.ipynb` — Complete Jupyter notebook with all 5 tasks (code + markdown)
- `task-statement.txt` — Original task instructions
- `notes.md` — Comprehensive notes covering all 5 tasks
- `week2_day1_writeup.pdf` — 1-page write-up covering ReAct loop, tool schemas, failure modes
- `week2_day1_writeup.md` — Markdown source for the write-up

## Final Code Structure

```python
# Agent loop core
while True:
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
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