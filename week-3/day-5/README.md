# Week 3 Day 5 — Capstone: Full AFL Assistant, Evaluation, Deployment

## Overview
Ship the complete product: domain-locked AFL chat + prediction assistant, evaluated, wrapped behind API/UI, with monitoring and stakeholder presentation.

## Tasks
1. System Hardening — Error handling, timeouts, disclaimers, prompt injection tests
2. Comprehensive Evaluation — 25+ test cases, results table, benchmark comparison
3. Wrap as API/UI — FastAPI endpoint, optional Streamlit UI, structured logging
4. Monitoring & Maintenance Plan — Checklist, retraining loop
5. Final Deliverables — Executive report PDF, demo script, slide outline

## Data
- `train.csv`, `val.csv`, `test.csv` — From Day 1
- `feature_table.csv` — From Day 1

## How to Run
```bash
# API
python api.py

# UI (optional)
streamlit run ui.py
```

## Deliverables
- Working LangGraph app + FastAPI wrapper
- 25+ test case results table
- Executive report PDF
- Demo script / slide outline
