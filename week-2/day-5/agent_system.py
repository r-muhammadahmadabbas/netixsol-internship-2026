"""
Week 2 Day 5 — Capstone: Client Inquiry Qualification Agent
============================================================
Web3Geeks client onboarding system using LangGraph.

Flow: Validate -> Research -> Qualify -> Draft -> Human Approve -> End
"""

import os
import json
import re
import time
import logging
from typing import TypedDict
from dotenv import load_dotenv

from langgraph.graph import StateGraph, END

load_dotenv(r"C:\Internship\Netixsol\week-2\day-5\.env")

# =============================================================================
# LOGGING
# =============================================================================
logging.basicConfig(
    filename=r"C:\Internship\Netixsol\week-2\day-5\agent_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# =============================================================================
# STATE
# =============================================================================
class InquiryState(TypedDict):
    inquiry_id: str
    name: str
    email: str
    company: str
    message: str
    company_info: dict
    qualification: str
    draft_response: str
    approved: bool
    status: str
    error: str
    tool_calls: list
    latency: float
    token_count: int

# =============================================================================
# LLM
# =============================================================================
import litellm
openrouter_key = os.getenv("OPENROUTER_API_KEY")

def call_llm(system_prompt: str, user_prompt: str) -> str:
    """Call LLM via litellm."""
    response = litellm.completion(
        model="openrouter/meta-llama/llama-3.3-70b-instruct",
        api_key=openrouter_key,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

# =============================================================================
# TOOLS
# =============================================================================
COMPANIES_DB = r"C:\Internship\Netixsol\week-2\day-5\companies.json"

def load_companies():
    with open(COMPANIES_DB, "r") as f:
        return json.load(f)["companies"]

def search_company(company_name: str) -> dict:
    companies = load_companies()
    for c in companies:
        if c["name"].lower() in company_name.lower() or company_name.lower() in c["name"].lower():
            return c
    return None

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

# =============================================================================
# NODES
# =============================================================================
def validate_input(state: InquiryState) -> InquiryState:
    start = time.time()
    errors = []

    if not state.get("name") or len(state["name"].strip()) < 2:
        errors.append("Name must be at least 2 characters")
    if not state.get("email") or not validate_email(state["email"]):
        errors.append("Invalid email format")
    if not state.get("message") or len(state["message"].strip()) < 10:
        errors.append("Message must be at least 10 characters")

    latency = time.time() - start
    logger.info(f"Validation completed in {latency:.3f}s - Errors: {len(errors)}")

    if errors:
        return {
            **state,
            "status": "error",
            "error": "; ".join(errors),
            "latency": latency,
            "tool_calls": state.get("tool_calls", []) + ["validate_input:FAIL"]
        }

    return {
        **state,
        "status": "valid",
        "error": "",
        "latency": latency,
        "tool_calls": state.get("tool_calls", []) + ["validate_input:PASS"]
    }

def research_company(state: InquiryState) -> InquiryState:
    start = time.time()
    company_name = state.get("company", "")

    if not company_name:
        logger.info("No company name provided, skipping research")
        return {
            **state,
            "company_info": {"name": "Unknown", "industry": "Unknown", "budget_range": "unknown"},
            "tool_calls": state.get("tool_calls", []) + ["research_company:NO_COMPANY"],
            "latency": state.get("latency", 0) + (time.time() - start)
        }

    company_info = search_company(company_name)
    latency = time.time() - start

    if company_info:
        logger.info(f"Found company: {company_name} in {latency:.3f}s")
        return {
            **state,
            "company_info": company_info,
            "tool_calls": state.get("tool_calls", []) + [f"research_company:FOUND:{company_name}"],
            "latency": state.get("latency", 0) + latency
        }
    else:
        logger.info(f"Company not found: {company_name}")
        return {
            **state,
            "company_info": {"name": company_name, "industry": "Unknown", "budget_range": "unknown"},
            "tool_calls": state.get("tool_calls", []) + [f"research_company:NOT_FOUND:{company_name}"],
            "latency": state.get("latency", 0) + latency
        }

def qualify_lead(state: InquiryState) -> InquiryState:
    start = time.time()

    company_info = state.get("company_info", {})
    budget_range = company_info.get("budget_range", "unknown")
    message = state.get("message", "").lower()

    score = 0
    if budget_range == "high":
        score += 3
    elif budget_range == "medium":
        score += 2
    elif budget_range == "low":
        score += 1

    if any(word in message for word in ["urgent", "asap", "immediately"]):
        score += 2
    if any(word in message for word in ["budget", "price", "cost", "quote"]):
        score += 1
    if any(word in message for word in ["web3", "blockchain", "smart contract", "defi", "nft"]):
        score += 2

    if score >= 5:
        qualification = "high"
    elif score >= 3:
        qualification = "medium"
    else:
        qualification = "low"

    latency = time.time() - start
    logger.info(f"Lead qualified: {qualification} (score={score}) in {latency:.3f}s")

    return {
        **state,
        "qualification": qualification,
        "tool_calls": state.get("tool_calls", []) + [f"qualify_lead:{qualification}:{score}"],
        "latency": state.get("latency", 0) + latency
    }

def draft_response(state: InquiryState) -> InquiryState:
    start = time.time()

    system_prompt = """You are a sales assistant for Web3Geeks, a web3 development agency.
    Draft a professional, personalized response to a client inquiry.
    Be concise, friendly, and specific to their needs."""

    user_prompt = f"""Client Inquiry:
    Name: {state['name']}
    Company: {state.get('company', 'N/A')}
    Industry: {state.get('company_info', {}).get('industry', 'Unknown')}
    Budget Range: {state.get('company_info', {}).get('budget_range', 'Unknown')}
    Message: {state['message']}

    Draft a response."""

    try:
        response_text = call_llm(system_prompt, user_prompt)
        latency = time.time() - start
        token_count = len(response_text.split())
        logger.info(f"Response drafted in {latency:.3f}s - ~{token_count} words")
        return {
            **state,
            "draft_response": response_text,
            "tool_calls": state.get("tool_calls", []) + ["draft_response:LLM_CALL"],
            "latency": state.get("latency", 0) + latency,
            "token_count": token_count
        }
    except Exception as e:
        latency = time.time() - start
        logger.error(f"LLM error: {str(e)}")
        return {
            **state,
            "draft_response": f"Error drafting response: {str(e)}",
            "tool_calls": state.get("tool_calls", []) + [f"draft_response:ERROR"],
            "latency": state.get("latency", 0) + latency
        }

def human_review(state: InquiryState) -> InquiryState:
    """Human-in-the-loop checkpoint. Auto-approves based on qualification."""
    if state.get("qualification") == "high":
        logger.info("Auto-approved: high qualification")
        return {**state, "approved": True, "status": "approved"}
    elif state.get("qualification") == "medium":
        logger.info("Auto-approved: medium qualification")
        return {**state, "approved": True, "status": "approved"}
    else:
        logger.info("Pending review: low qualification")
        return {**state, "approved": False, "status": "pending_review"}

def handle_error(state: InquiryState) -> InquiryState:
    logger.warning(f"Error handled: {state.get('error', 'Unknown')}")
    return {
        **state,
        "status": "error",
        "draft_response": f"We encountered an issue: {state.get('error', 'Unknown error')}. Please try again.",
        "tool_calls": state.get("tool_calls", []) + ["handle_error"]
    }

# =============================================================================
# ROUTING
# =============================================================================
def route_after_validation(state: InquiryState) -> str:
    if state.get("status") == "error":
        return "error_handler"
    return "research"

def route_after_qualification(state: InquiryState) -> str:
    if state.get("qualification") == "low":
        return "error_handler"
    return "draft"

# =============================================================================
# GRAPH
# =============================================================================
workflow = StateGraph(InquiryState)

workflow.add_node("validate", validate_input)
workflow.add_node("research", research_company)
workflow.add_node("qualify", qualify_lead)
workflow.add_node("draft", draft_response)
workflow.add_node("human_review", human_review)
workflow.add_node("error_handler", handle_error)

workflow.set_entry_point("validate")

workflow.add_conditional_edges(
    "validate",
    route_after_validation,
    {"research": "research", "error_handler": "error_handler"}
)

workflow.add_edge("research", "qualify")

workflow.add_conditional_edges(
    "qualify",
    route_after_qualification,
    {"draft": "draft", "error_handler": "error_handler"}
)

workflow.add_edge("draft", "human_review")
workflow.add_edge("human_review", END)
workflow.add_edge("error_handler", END)

app = workflow.compile()

# =============================================================================
# RUN
# =============================================================================
if __name__ == "__main__":
    test_inquiry = {
        "inquiry_id": "INQ-001",
        "name": "John Smith",
        "email": "john@techcorp.com",
        "company": "TechCorp Solutions",
        "message": "We need a web3 integration for our enterprise platform. Looking for smart contract development and DeFi features. Budget is flexible."
    }

    print("=" * 60)
    print("CLIENT INQUIRY QUALIFICATION SYSTEM")
    print("=" * 60)

    result = app.invoke(test_inquiry)

    print(f"\nStatus: {result['status']}")
    print(f"Qualification: {result.get('qualification', 'N/A')}")
    print(f"Approved: {result.get('approved', 'N/A')}")
    print(f"Latency: {result.get('latency', 0):.2f}s")
    print(f"Tool calls: {result.get('tool_calls', [])}")
    print(f"\nDraft Response:\n{result.get('draft_response', 'N/A')}")
