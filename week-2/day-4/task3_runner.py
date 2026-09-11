"""
Week 2 Day 4 — CrewAI: Multi-Agent Collaboration
Task 3: Define Tasks & Process
--------------------------------------------------
Business task: Research Canva, analyze findings, draft marketing angle.

Fixes applied for CrewAI v1.15.x + Groq/OpenRouter:
1. cache_breakpoint monkey-patch (Groq doesn't support it)
2. executor_type="crew" (avoids experimental executor adding built-in tools)
3. max_iter=5 (prevents infinite tool-call loops)
4. OpenRouter instead of Groq (Groq free tier 8000 TPM is too low)
5. UTF-8 encoding for print (Windows cp1252 can't handle unicode)
"""

import os
from crewai import Agent, Task, Crew, LLM, Process
from crewai.tools import tool
from dotenv import load_dotenv

# Fix 1: Strip cache_breakpoint (CrewAI sends it, Groq/OpenRouter don't support it)
import crewai.llms.cache as _cache
_cache.mark_cache_breakpoint = lambda msg: msg

load_dotenv(r"C:\Internship\Netixsol\week-2\day-4\.env")
openrouter_key = os.getenv("OPENROUTER_API_KEY")

# =============================================================================
# LLM CONFIG — one per agent, different temperatures
# =============================================================================
# Researcher: temp=0 (factual, no randomness)
# Analyst: temp=0.3 (structured, slight flexibility)
# Strategist: temp=0.7 (creative, needs variety)
researcher_llm = LLM(model="openrouter/meta-llama/llama-3.3-70b-instruct", temperature=0.0, api_key=openrouter_key)
analyst_llm = LLM(model="openrouter/meta-llama/llama-3.3-70b-instruct", temperature=0.3, api_key=openrouter_key)
strategist_llm = LLM(model="openrouter/meta-llama/llama-3.3-70b-instruct", temperature=0.7, api_key=openrouter_key)

# =============================================================================
# TOOLS
# =============================================================================
@tool("web_search")
def web_search(query: str) -> str:
    """Search the web for information about a query."""
    return f"Search results for '{query}': Found competitor pricing, features, and market position data."

@tool("write_file")
def write_file(file_path: str, content: str) -> str:
    """Write content to a file and confirm success."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Successfully wrote to {file_path}"

# =============================================================================
# AGENTS — each with role, goal, backstory, tools
# =============================================================================
# Fix 2: executor_type="crew" avoids experimental executor adding built-in tools
# Fix 3: max_iter=5 prevents infinite tool-call loops

researcher = Agent(
    role="Competitor Research Specialist",
    goal="Gather accurate, well-sourced factual information about the competitor.",
    backstory="You are a former competitive-intelligence analyst who is strictly factual.",
    llm=researcher_llm,
    tools=[web_search],
    verbose=True,
    allow_delegation=False,
    executor_type="crew",
    max_iter=5,
)

analyst = Agent(
    role="Competitive Insights Analyst",
    goal="Distill raw research into a structured summary with strengths, weaknesses, and opportunities.",
    backstory="You are a data-driven analyst who turns raw information into strategic insights.",
    llm=analyst_llm,
    tools=[write_file],
    verbose=True,
    allow_delegation=False,
    executor_type="crew",
    max_iter=5,
)

strategist = Agent(
    role="Marketing Angle Strategist",
    goal="Turn a structured competitive summary into a sharp, differentiated marketing angle.",
    backstory="You are a copywriting specialist who builds directly on analysis.",
    llm=strategist_llm,
    tools=[write_file],
    verbose=True,
    allow_delegation=False,
    executor_type="crew",
    max_iter=5,
)

# =============================================================================
# TASKS — connected via context dependencies
# =============================================================================
# Task 1: Researcher produces raw data
# Task 2: Analyst receives Researcher's output via context=[research_task]
# Task 3: Strategist receives Analyst's output via context=[analysis_task]

research_task = Task(
    description=(
        "Research Canva (the design tool company). Find: "
        "1) Their main products and features, "
        "2) Pricing tiers, "
        "3) Market position and target audience, "
        "4) Recent news or updates in 2024-2025."
    ),
    expected_output="A structured report with 4 sections: Products, Pricing, Market Position, Recent News. Each section has 3-5 bullet points with specific details.",
    agent=researcher,
)

analysis_task = Task(
    description=(
        "Using the research findings, create a SWOT analysis "
        "(Strengths, Weaknesses, Opportunities, Threats). "
        "Identify 3 key insights that could inform our marketing strategy."
    ),
    expected_output="A SWOT analysis with 3-4 items per category, followed by 3 numbered key insights. Each insight is one paragraph.",
    agent=analyst,
    context=[research_task],
)

strategy_task = Task(
    description=(
        "Using the analysis, draft 2-3 marketing angles for competing against Canva. "
        "For each: provide a headline, key message, target audience, and why it works. "
        "Pick the strongest angle."
    ),
    expected_output="2-3 marketing angles with Headline, Key Message, Target Audience, Why It Works. End with a recommendation paragraph.",
    agent=strategist,
    context=[analysis_task],
)

# =============================================================================
# ASSEMBLE CREW & RUN
# =============================================================================
crew = Crew(
    agents=[researcher, analyst, strategist],
    tasks=[research_task, analysis_task, strategy_task],
    process=Process.sequential,
    verbose=True,
)

print("=" * 60)
print("RUNNING CREWAI CREW (SEQUENTIAL)")
print("=" * 60)
result = crew.kickoff()

print("\n" + "=" * 60)
print("FINAL OUTPUT")
print("=" * 60)
print(str(result).encode("utf-8", errors="replace").decode("utf-8"))
