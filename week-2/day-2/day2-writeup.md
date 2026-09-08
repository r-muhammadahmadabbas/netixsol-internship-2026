# Week 2 Day 2 — Raw Python vs LangChain Agent Comparison

## Agent Architecture Comparison

### Raw Python Agent (Day 1)
- **Tool Registration**: Manual JSON schema dictionaries per tool
- **Agent Loop**: Explicit `while True` loop with manual break conditions
- **Tool Routing**: Manual `if tool_name in tool_schemas` checking
- **Memory**: Manual `messages` list appended after each turn
- **Error Handling**: Manual `try/except` blocks around each tool call
- **Max Iterations**: Manual counter `iteration < max_iterations`

### LangChain Agent (Day 2)
- **Tool Registration**: `@tool` decorator auto-generates schema from signature + docstring
- **Agent Loop**: `create_agent()` returns compiled graph — loop is internal
- **Tool Routing**: LLM sees tool descriptions (from docstrings) and picks tool
- **Memory**: `MemorySaver` + `thread_id` config — automatic persistence
- **Error Handling**: Built-in error wrapping — failures become tool observations
- **Max Iterations**: Handled internally by graph execution

## Side-by-Side Code Comparison

```python
# RAW PYTHON (Day 1) — Agent loop
messages = []
max_iterations = 5
for i in range(max_iterations):
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        tools=tool_schemas,
        messages=messages
    )
    if response.stop_reason == "end_turn":
        break
    for block in response.content:
        if block.type == "tool_use":
            result = execute_tool(block.name, block.input)
            messages.append({"role": "tool", ...})
    messages.append({"role": "assistant", ...})

# LANGCHAIN (Day 2) — Agent loop
agent = create_agent(model=llm, tools=tools, debug=True)
result = agent.invoke({"messages": [{"role": "user", "content": "..." }]})
```

## What LangChain Made Easier
1. **Tool registration** — `@tool` decorator replaces 15-line JSON schemas per tool
2. **Agent loop** — No manual `while` loop, break conditions, or iteration counters
3. **Memory** — `MemorySaver` + `thread_id` replaces manual `messages` list management
4. **Error handling** — Tool failures automatically become observations for the LLM
5. **Debugging** — `debug=True` shows full reasoning trace without custom print statements

## Structured Output Approach (Task 5)

Groq doesn't support `response_format` with tools, so we used a **two-step approach**:

1. **Agent gathers data** via tools (normal agent loop)
2. **Separate LLM chain forces JSON** via explicit prompt + Pydantic parsing

```python
# Pydantic schema defines the output structure
class ProductRecommendation(BaseModel):
    product: str
    price: float
    reason: str

# Chain with no tools — just prompt → LLM → parse JSON
structured_prompt = ChatPromptTemplate.from_messages([
    ("system", "Respond with ONLY JSON: product, price, reason."),
    ("user", "{context}")
])
chain = structured_prompt | llm
raw = chain.invoke({"context": agent_output}).content
parsed = ProductRecommendation.model_validate_json(raw)
```

**Key insight**: Structured output via `response_format` requires tool-calling support. When your LLM provider doesn't support it (like Groq), use prompt engineering + Pydantic validation instead.

## Abstraction Leakiness / Hidden Complexity
1. **Hidden prompt templates** — LangChain constructs system prompts you can't easily inspect
2. **Argument parsing** — Tool input extraction happens internally, hard to customize
3. **Message formatting** — How history is injected into context is opaque
4. **Groq incompatibility** — `response_format` (structured output) doesn't work with Groq's API when tools are bound — requires workaround

## Annotated Reasoning Trace (from Task 3)

```
User: "What's the weather in Tokyo and Paris? Which is warmer?"

Thought: I need to look up weather for Tokyo first          ← REASONING
Action: get_weather                                         ← ACT
Action Input: {"city": "Tokyo"}                             ← ARGUMENT
Observation: Weather in Tokyo: 22°C                         ← OBSERVE

Thought: Now I need Paris weather to compare                ← REASONING
Action: get_weather                                         ← ACT
Action Input: {"city": "Paris"}                             ← ARGUMENT
Observation: Weather in Paris: 18°C                         ← OBSERVE

Thought: Tokyo (22°C) is warmer than Paris (18°C)          ← REASONING
Final Answer: Tokyo is warmer at 22°C vs Paris at 18°C     ← FINAL
```

**Similar to Day 1**: Same Thought → Act → Observe cycle. **Hidden**: Prompt template construction, argument parsing, message formatting.
