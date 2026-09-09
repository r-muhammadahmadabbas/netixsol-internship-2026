# =============================================================================
# Task 1: Graph Concepts & State Design
# =============================================================================
# Before coding the actual graph, we design it:
# 1. Define the State schema (what data flows through)
# 2. Draw the graph (ASCII diagram)
# 3. Verify the State schema works

from typing import TypedDict, Annotated
import operator

# =============================================================================
# STEP 1: Define the State Schema
# =============================================================================
# This is the "blueprint" — what data our graph will carry.
# We're building a Research Assistant that:
#   1. Takes a user query
#   2. Creates a plan
#   3. Executes the plan (search + retrieve)
#   4. Generates an answer
#   5. Critiques the answer
#   6. If bad → retry (loop back to execute)
#   7. If good → finish

class ResearchState(TypedDict):
    """State schema for our Research Assistant graph."""
    
    # --- Input ---
    query: str                          # What the user asked
    
    # --- Pipeline outputs ---
    plan: str                           # What the agent plans to do
    search_results: str                 # Raw results from tools
    answer: str                         # Generated answer
    critique: str                       # Quality feedback
    quality_score: int                  # Score 0-10 (10 = perfect)
    
    # --- Control flow ---
    retry_count: int                    # How many times we retried
    max_retries: int                    # Safety limit (prevent infinite loops)
    messages: Annotated[list, operator.add]  # Conversation history


# =============================================================================
# STEP 2: Draw the Graph (ASCII Diagram)
# =============================================================================
# We draw this BEFORE writing any node code.

diagram = """
+-------------------------------------------------------------------+
|                    RESEARCH ASSISTANT GRAPH                        |
+-------------------------------------------------------------------+
|                                                                    |
|  +----------+                                                     |
|  |  START   |                                                     |
|  +----+-----+                                                     |
|       |                                                            |
|       v                                                            |
|  +----------+    "Create a plan based on the query"               |
|  |   PLAN   +----------------------------------------+            |
|  +----+-----+                                        |            |
|       |                                              |            |
|       v                                              |            |
|  +----------+    "Search and retrieve info"          |            |
|  | EXECUTE  |<-------------------------------+      |            |
|  +----+-----+                                |      |            |
|       |                                      |      |            |
|       v                                      |      |            |
|  +----------+    "Write an answer"           |      |            |
|  | GENERATE +--------------------------------+      |            |
|  +----+-----+                                |      |            |
|       |                                      |      |            |
|       v                                      |      |            |
|  +----------+    "Rate quality 0-10"         |      |            |
|  | CRITIQUE +--------------------------------+      |            |
|  +----+-----+                                      |            |
|       |                                            |            |
|       | if score < 7 AND retries < max             |            |
|       +-------------- RETRY LOOP ------------------+            |
|                                                                    |
|       | if score >= 7 OR retries >= max                           |
|       v                                                            |
|  +----------+                                                     |
|  |  FINISH  |                                                     |
|  +----------+                                                     |
|                                                                    |
+-------------------------------------------------------------------+
"""

print(diagram)


# =============================================================================
# STEP 3: Verify the State Schema Works
# =============================================================================
# Create a sample state and check it has all required fields.

sample_state: ResearchState = {
    "query": "What is LangGraph and how is it different from LangChain?",
    "plan": "",
    "search_results": "",
    "answer": "",
    "critique": "",
    "quality_score": 0,
    "retry_count": 0,
    "max_retries": 3,
    "messages": [],
}

print("=" * 60)
print("STATE SCHEMA VERIFICATION")
print("=" * 60)
print(f"Fields in ResearchState: {list(ResearchState.__annotations__.keys())}")
print(f"Sample state created with {len(sample_state)} fields")
print()

# Show what each field is for
print("Field descriptions:")
print("-" * 40)
for field, field_type in ResearchState.__annotations__.items():
    print(f"  {field:20s} -> {field_type}")
print()

# Simulate a node updating state
print("Simulating node update:")
print("-" * 40)

def plan_node(state: ResearchState) -> dict:
    """Example plan node — reads query, returns a plan."""
    query = state["query"]
    plan = f"Step 1: Search for '{query}'\nStep 2: Summarize findings\nStep 3: Compare with Day 2 concepts"
    return {"plan": plan}

# Run the node
update = plan_node(sample_state)
print(f"  Input query: {sample_state['query']}")
print(f"  Node returned: {update}")
print()

# Merge update into state (this is what LangGraph does automatically)
sample_state.update(update)
print(f"  State after merge: plan = '{sample_state['plan'][:60]}...'")
print()

# Show that other fields are unchanged
print("Other fields unchanged:")
print(f"  query: '{sample_state['query'][:40]}...'")
print(f"  quality_score: {sample_state['quality_score']}")
print(f"  retry_count: {sample_state['retry_count']}")
