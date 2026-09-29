"""
Week 3 Day 5: Capstone - Full AFL Assistant
System hardening, evaluation, API, monitoring
"""
import os
import sys
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from day4.langgraph_agent import run_agent
from day2.predict import predict_match_winner, predict_top_player

# ============================================================================
# SYSTEM HARDENING
# ============================================================================

class HardenedAFLAssistant:
    """Production-ready AFL assistant with error handling and guardrails"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.off_topic_count = 0
        self.max_off_topic = 3
    
    def chat(self, message: str) -> Dict:
        """Process message with full error handling"""
        try:
            # Input validation
            if not message or not message.strip():
                return self._error_response("Kuch message likhein.")
            
            if len(message) > 1000:
                return self._error_response("Message bohat lamba hai. Chota karein.")
            
            # Rate limiting for off-topic
            if self._is_off_topic(message):
                self.off_topic_count += 1
                if self.off_topic_count >= self.max_off_topic:
                    return self._error_response("Aap bohat baar off-topic baat kar rahe hain. Kya main aapko AFL mein madad kar sakta hoon?")
            
            # Process
            result = run_agent(message)
            
            # Add disclaimer for predictions
            if result.get("intent") == "prediction":
                result["response"] += "\n\n*Yeh prediction historical data par based hai, certainty nahi.*"
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return self._error_response("Kuch error hua. Dobara try karein.")
    
    def _is_off_topic(self, message: str) -> bool:
        off_topic = ['weather', 'politics', 'cricket', 'movie', 'khana']
        return any(kw in message.lower() for kw in off_topic)
    
    def _error_response(self, message: str) -> Dict:
        return {
            "response": message,
            "intent": "error",
            "needs_clarification": False
        }

# ============================================================================
# EVALUATION SUITE
# ============================================================================

EVALUATION_CASES = [
    # Factual Q&A (8)
    {"id": "F01", "category": "factual", "input": "How many goals did Tony Lockett kick?", "expected": "goals"},
    {"id": "F02", "category": "factual", "input": "Collingwood ka record kya hai?", "expected": "record"},
    {"id": "F03", "category": "factual", "input": "Who won the 2023 Grand Final?", "expected": "winner"},
    {"id": "F04", "category": "factual", "input": "Patrick Cripps ki stats kya hain?", "expected": "stats"},
    {"id": "F05", "category": "factual", "input": "DHA Phase 5 mein kya facilities hain?", "expected": "facilities"},
    {"id": "F06", "category": "factual", "input": "AFL season mein kitne rounds hote hain?", "expected": "rounds"},
    {"id": "F07", "category": "factual", "input": "Brownlow Medal kya hai?", "expected": "brownlow"},
    {"id": "F08", "category": "factual", "input": "Home ground advantage kya hai?", "expected": "advantage"},
    
    # Prediction (6)
    {"id": "P01", "category": "prediction", "input": "Who will win Collingwood vs Carlton?", "expected": "prediction"},
    {"id": "P02", "category": "prediction", "input": "Predict Richmond vs Hawthorn", "expected": "prediction"},
    {"id": "P03", "category": "prediction", "input": "Who will top-score in Geelong vs Sydney?", "expected": "top_player"},
    {"id": "P04", "category": "prediction", "input": "Collingwood vs Carlton ka prediction do", "expected": "prediction"},
    {"id": "P05", "category": "prediction", "input": "Will Hawthorn beat Richmond?", "expected": "prediction"},
    {"id": "P06", "category": "prediction", "input": "Top player predict karo Brisbane vs Sydney", "expected": "top_player"},
    
    # Off-Topic (5)
    {"id": "O01", "category": "off_topic", "input": "What's the weather like?", "expected": "refusal"},
    {"id": "O02", "category": "off_topic", "input": "Who won the cricket match?", "expected": "refusal"},
    {"id": "O03", "category": "off_topic", "input": "Tell me about politics", "expected": "refusal"},
    {"id": "O04", "category": "off_topic", "input": "What's for dinner?", "expected": "refusal"},
    {"id": "O05", "category": "off_topic", "input": "Play a song", "expected": "refusal"},
    
    # Multi-Turn (4)
    {"id": "M01", "category": "multi_turn", "input": "Collingwood ke baare mein batao", "expected": "context"},
    {"id": "M02", "category": "multi_turn", "input": "Unka captain kaun hai?", "expected": "context"},
    {"id": "M03", "category": "multi_turn", "input": "Kitne premierships hain?", "expected": "context"},
    {"id": "M04", "category": "multi_turn", "input": "Best player kaun hai?", "expected": "context"},
]

def run_evaluation():
    """Run full evaluation suite"""
    assistant = HardenedAFLAssistant()
    results = []
    
    print("\n" + "=" * 60)
    print("  EVALUATION SUITE")
    print("=" * 60 + "\n")
    
    for test in EVALUATION_CASES:
        result = assistant.chat(test["input"])
        passed = result.get("intent") != "error"
        
        results.append({
            "id": test["id"],
            "category": test["category"],
            "input": test["input"],
            "passed": passed,
            "response": result.get("response", "")[:50]
        })
        
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status} {test['id']} ({test['category']}): {test['input'][:40]}...")
    
    # Summary
    categories = {}
    for r in results:
        cat = r["category"]
        if cat not in categories:
            categories[cat] = {"total": 0, "passed": 0}
        categories[cat]["total"] += 1
        if r["passed"]:
            categories[cat]["passed"] += 1
    
    print("\n" + "=" * 60)
    print("  RESULTS")
    print("=" * 60)
    
    total_passed = 0
    total_tests = 0
    for cat, stats in categories.items():
        rate = stats["passed"] / stats["total"] * 100
        print(f"  {cat}: {stats['passed']}/{stats['total']} ({rate:.0f}%)")
        total_passed += stats["passed"]
        total_tests += stats["total"]
    
    print(f"\n  TOTAL: {total_passed}/{total_tests} ({total_passed/total_tests*100:.0f}%)")
    print("=" * 60 + "\n")
    
    return results

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    run_evaluation()