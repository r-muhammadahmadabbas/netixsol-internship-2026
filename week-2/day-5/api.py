"""
Week 2 Day 5 — Capstone: FastAPI Wrapper
==========================================
Expose the agent system via a simple API endpoint.
"""

import os
import sys
import time
import logging
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

load_dotenv(r"C:\Internship\Netixsol\week-2\day-5\.env")

# Import the agent system
sys.path.insert(0, r"C:\Internship\Netixsol\week-2\day-5")
from agent_system import app

# =============================================================================
# LOGGING
# =============================================================================
logging.basicConfig(
    filename=r"C:\Internship\Netixsol\week-2\day-5\api_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# =============================================================================
# MODELS
# =============================================================================
class InquiryRequest(BaseModel):
    inquiry_id: str
    name: str
    email: str
    company: Optional[str] = ""
    message: str

class InquiryResponse(BaseModel):
    inquiry_id: str
    status: str
    qualification: Optional[str] = None
    approved: Optional[bool] = None
    draft_response: Optional[str] = None
    latency: float
    tool_calls: list
    error: Optional[str] = None

# =============================================================================
# APP
# =============================================================================
app_api = FastAPI(
    title="Web3Geeks Client Inquiry API",
    description="Qualify client inquiries using AI agents",
    version="1.0.0"
)

@app_api.post("/qualify", response_model=InquiryResponse)
async def qualify_inquiry(request: InquiryRequest):
    """Qualify a client inquiry using the agent system."""
    start = time.time()
    
    logger.info(f"Request received: {request.inquiry_id} from {request.email}")
    
    try:
        result = app.invoke(request.dict())
        latency = time.time() - start
        
        logger.info(f"Request completed: {request.inquiry_id} - Status: {result['status']} - Latency: {latency:.2f}s")
        
        return InquiryResponse(
            inquiry_id=result["inquiry_id"],
            status=result["status"],
            qualification=result.get("qualification"),
            approved=result.get("approved"),
            draft_response=result.get("draft_response"),
            latency=latency,
            tool_calls=result.get("tool_calls", []),
            error=result.get("error")
        )
    except Exception as e:
        latency = time.time() - start
        logger.error(f"Request failed: {request.inquiry_id} - Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app_api.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Web3Geeks Client Inquiry API"}

# =============================================================================
# RUN
# =============================================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app_api, host="0.0.0.0", port=8000)
