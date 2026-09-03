# Day 4 — Model Tuning, Regularization & Reproducible Pipelines

## Status: IN PROGRESS

## What We're Doing Today

| Task | Description | Status |
|------|-------------|--------|
| 1 | Build Fully Reproducible Pipelines | 🔲 |
| 2 | Hyperparameter Search (Randomized/Grid) | 🔲 |
| 3 | Diagnose Overfitting / Underfitting | 🔲 |
| 4 | Probability Calibration & Threshold Selection | 🔲 |
| 5 | Final Evaluation & Save Artifact | 🔲 |

## Deliverables
- `day4-soln.ipynb` — notebook with all 5 tasks
- `day4-tuning-report.pdf` — 1-2 page tuning report
- `day4-final-pipeline.joblib` — saved model artifact

## Key Concepts Today
- **Reproducible Pipelines**: Fixed random states, documented versions
- **Hyperparameter Search**: RandomizedSearchCV/GridSearchCV with StratifiedKFold
- **Learning Curves**: Diagnose bias vs variance
- **Calibration**: Brier score, isotonic/sigmoid calibration
- **Threshold Tuning**: Optimize for business metric (precision)
- **Model Artifacts**: Save pipeline with joblib for production

## Primary Metric
Precision (same as Day 1-3) — business goal: minimize wasted outreach on low earners.

## Baseline from Day 3
- HistGradientBoosting: Precision 0.7758 ± 0.0073, ROC AUC 0.9255 ± 0.0025
- Logistic Regression: Precision 0.7455 ± 0.0083, ROC AUC 0.9130 ± 0.0045
- Features to keep: log_capital_gain, edu_hours_interaction, higher_ed, age_group_40-54, capital_gain, education_num, hours_per_week, marital status, occupation
- Features to drop: has_capital_gain (redundant), fnlwgt, weak native-country bins

## Models to Tune
1. **HistGradientBoosting** (primary - Day 3 winner)
2. **Logistic Regression** (baseline - with L1/L2 regularization)
3. **Random Forest** (ensemble baseline)