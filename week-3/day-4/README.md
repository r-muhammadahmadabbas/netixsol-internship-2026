# Week 3 Day 4 — LangGraph Integration: Routing Between Chat, Retrieval & Prediction

## Overview
Connect everything: chat agent (Day 3) + prediction models (Day 2) + LangGraph orchestration.

## Tasks
1. Graph Design — State schema, routing nodes, justification
2. Router Node — Intent classifier, 15-20 test queries
3. Wire Prediction Models — wrap Day 2 functions as tools
4. Self-Correction & Fallbacks — validation node, error handling
5. End-to-End Testing — 10 conversations, state traces, comparison

## Data
- `train.csv`, `val.csv`, `test.csv` — From Day 1
- `feature_table.csv` — From Day 1

## How to Run
```bash
jupyter notebook
```

## Deliverables
- Working LangGraph application
- Annotated state traces
- Routing accuracy table
