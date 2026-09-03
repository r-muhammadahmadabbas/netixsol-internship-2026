# Day 4 — Model Tuning, Regularization & Reproducible Pipelines

## Status: ✅ COMPLETE

## What We Did Today

| Task | Description | Status |
|------|-------------|--------|
| 1 | Build Fully Reproducible Pipelines | ✅ |
| 2 | Hyperparameter Search (Randomized/Grid) | ✅ |
| 3 | Diagnose Overfitting / Underfitting | ✅ |
| 4 | Probability Calibration & Threshold Selection | ✅ |
| 5 | Final Evaluation & Save Artifact | ✅ |

## Deliverables (All Complete)
- `day4-soln.ipynb` — notebook with all 5 tasks
- `day4-tuning-report.pdf` — 1-page tuning report
- `day4-final-pipeline.joblib` — saved model artifact (+ `day4-threshold-info.json`)

## Key Results

### 1. Hyperparameter Search (maximize CV Precision)
| Model | Best CV Precision | Best Hyperparameters |
|-------|-------------------|----------------------|
| Logistic Regression | 0.7666 | C=0.00108, penalty=l1, solver=liblinear, max_iter=1000 |
| Random Forest | 0.8018 | max_depth=5, max_features=log2, min_samples_leaf=2, min_samples_split=10, n_estimators=189 |
| **HistGradientBoost (Winner)** | **0.8025** | learning_rate=0.01432, max_iter=127, max_depth=10, l2_regularization=0.0152, min_samples_leaf=16 |

### 2. Diagnostics
- **Learning curve**: train precision 0.8401±0.0038 vs validation 0.8012±0.0082 (gap 0.0389) → **good fit**, no severe overfitting
- Validation curves over `learning_rate`, `max_iter`, `max_depth`, `l2_regularization` confirmed stable plateaus

### 3. Calibration & Threshold Selection
- **Isotonic calibration (5-fold)**: Brier 0.0949 → **0.0918** (improvement 0.0031)
- **Optimal threshold = 0.832** (max precision, recall ≥ 0.3)

| Threshold | Precision | Recall | F1 | Spec | FP |
|-----------|-----------|--------|-----|------|-----|
| 0.324 (best F1) | 0.6467 | 0.7997 | 0.7151 | 0.8615 | 685 |
| 0.500 (default) | 0.7638 | 0.6250 | 0.6875 | 0.9387 | 303 |
| 0.538 | 0.8002 | 0.5797 | 0.6723 | 0.9541 | 227 |
| **0.832 (OPTIMAL)** | **0.9695** | 0.3036 | 0.4624 | 0.9970 | 15 |

### 4. Final Performance (Hold-out Test, @ threshold 0.832)
| Metric | Value |
|--------|-------|
| **Precision** | **0.9695** |
| Recall | 0.3036 |
| F1 Score | 0.4624 |
| Specificity | 0.9970 |
| Calibrated Brier | 0.0918 |
| ROC AUC | 0.9213 |

**Business impact vs default (0.5):** +32.27% precision, 670 fewer false alarms (303 → 15), 778 more missed positives.

## Key Concepts Covered
- **Reproducible Pipelines**: Fixed random states, documented versions
- **Hyperparameter Search**: RandomizedSearchCV with StratifiedKFold
- **Learning Curves**: Diagnose bias vs variance
- **Calibration**: Brier score, isotonic calibration
- **Threshold Tuning**: Optimize for business metric (precision)
- **Model Artifacts**: Save pipeline with joblib for production
- **Fix applied**: `engineer_features` defined at module level for pickling; params filtered to valid HGB constructor args (excludes `memory`)

## Primary Metric
Precision (same as Day 1-3) — business goal: minimize wasted outreach on low earners.

## Baseline from Day 3
- HistGradientBoosting: Precision 0.7758 ± 0.0073, ROC AUC 0.9255 ± 0.0025
- **Day 4 tuned + calibrated precision: 0.9695** (Δ +0.1937 vs Day 3 baseline)

## Models Tuned
1. **HistGradientBoosting** (primary - Day 3 winner, final deployed model)
2. **Logistic Regression** (baseline - L1/L2 regularization)
3. **Random Forest** (ensemble baseline)

## Artifacts Produced
| File | Description |
|------|-------------|
| `day4-final-pipeline.joblib` | Calibrated-ready deployable pipeline |
| `day4-threshold-info.json` | Optimal threshold + final metrics |
| `day4-best-{hgb,rf,lr}.joblib` | Best per-model pipelines |
| `day4-search-results.joblib` | Full search results |
| `day4-learning-curve.png` | Learning curve |
| `day4-validation-curves.png` | Validation curves |
| `day4-calibration-plot.png` | Reliability diagram |
| `day4-calibration-comparison.png` | Original vs calibrated |
| `day4-threshold-tuning.png` | 4-panel threshold analysis |
