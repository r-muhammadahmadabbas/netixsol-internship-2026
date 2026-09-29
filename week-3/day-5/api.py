"""
Week 3 Day 5: FastAPI Backend
REST API for the AFL Assistant
"""
import os
import sys
import logging
from datetime import datetime
from typing import Optional, List, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from day4.langgraph_agent import run_agent
from day2.predict import predict_match_winner, predict_top_player

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AFL Assistant API",
    description="Domain-locked AFL chat + prediction API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# MODELS
# ============================================================================

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    intent: str
    needs_clarification: bool = False

class PredictionRequest(BaseModel):
    team_a: str
    team_b: str

class PredictionResponse(BaseModel):
    winner: str
    probability: float
    confidence: str
    disclaimer: str

# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    return {"name": "AFL Assistant API", "version": "1.0.0", "docs": "/docs"}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint"""
    try:
        result = run_agent(request.message)
        return ChatResponse(
            response=result["response"],
            intent=result["intent"],
            needs_clarification=result.get("needs_clarification", False)
        )
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/match", response_model=PredictionResponse)
async def predict_match(request: PredictionRequest):
    """Predict match winner"""
    try:
        result = predict_match_winner(request.team_a, request.team_b)
        return PredictionResponse(
            winner=result["winner"],
            probability=result["probability"],
            confidence=result["confidence"],
            disclaimer="This is a prediction based on historical data, not a certainty."
        )
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/player")
async def predict_player(team: str, stat_type: str = "disposals"):
    """Predict top player"""
    try:
        results = predict_top_player(team=team, stat_type=stat_type)
        return {"players": results}
    except Exception as e:
        logger.error(f"Player prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)