# Week 4 Day 2 — Knowledge Base, RAG & Property Intelligence

## Overview
Build the knowledge base and RAG pipeline to ensure the agent never hallucinates property details.

## Tasks
1. **Design Knowledge Base** — Create datasets for properties, prices, locations, amenities, schools, hospitals, payment plans, developers, FAQs
2. **Build RAG Pipeline** — Document loader, chunking, embedding, vector store, retriever, answer generation
3. **Structured Retrieval** — Separate SQL (prices, availability) from vector search (descriptions, FAQs)
4. **Property Recommendation Engine** — Multi-criteria recommendation logic
5. **Hallucination Evaluation** — 20 questions, measure grounding, retrieval accuracy, hallucination rate

## Deliverables
- Property datasets (CSV/JSON)
- RAG pipeline implementation
- Retrieval comparison report
- Recommendation engine
- Hallucination evaluation results

## How to Run
```bash
# View datasets
ls day-2/data/
```