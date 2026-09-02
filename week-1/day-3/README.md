# Day 3 — Feature Engineering & Cross-Validation

## Status: IN PROGRESS

## What We're Doing Today

| Task | Description | Status |
|------|-------------|--------|
| 1 | Create & justify 6+ engineered features | 🔲 |
| 2 | Rebuild pipeline with engineered features | 🔲 |
| 3 | Cross-validated model comparison (3 models, 5-fold) | 🔲 |
| 4 | Statistical test (Wilcoxon) + feature importance | 🔲 |
| 5 | Feature selection / dimensionality check | 🔲 |

## Deliverables
- `day3-soln.ipynb` — notebook with all 5 tasks
- `day3-writeup.pdf` — 2-page summary

## Key Concepts Today
- **Feature Engineering:** Creating new columns from existing ones to help models learn patterns
- **Mutual Information:** Scoring how informative each feature is about the target
- **Cross-Validation:** 5-fold Stratified CV for reliable performance estimates
- **Wilcoxon Test:** Statistical test to check if model differences are real or noise
- **Feature Selection:** Removing weak features to reduce noise and speed up training

## Primary Metric
Precision (same as Day 1-2) — business goal: minimize wasted outreach on low earners.

## Baseline from Day 2
- Logistic Regression: Precision 0.743, F1 0.663, ROC AUC 0.906
- Decision Tree: Precision 0.617, F1 0.628 (overfits)
