# Week 1 — Machine Learning Internship: UCI Adult Income Prediction

## Status: ✅ COMPLETE (5/5 Days)

## Intern
Muhammad Ahmad Abbas — NetixSol Internship, Week 1 (Sep 1–5, 2026)

## Project Overview

Build a machine learning model to predict whether a person earns more than $50,000 per year based on demographic and employment data from the UCI Adult Census dataset. The primary business goal is to **maximize precision** — minimize wasted outreach by only contacting people who are very likely high earners.

## Dataset

- **Source**: UCI Machine Learning Repository (Adult/Census Income)
- **URL**: https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data
- **Total rows**: 48,842 (after dropping missing values)
- **Features**: 14 raw columns + 7 engineered = 21 columns
  - Numeric: age, fnlwgt, education_num, capital_gain, capital_loss, hours_per_week
  - Categorical: workclass, education, marital_status, occupation, relationship, race, sex, native_country
- **Engineered features** (Day 3): log_capital_gain, has_capital_gain, has_capital_loss, age_group, hours_category, higher_ed, edu_hours_interaction
- **Preprocessing output**: ~122 features after one-hot encoding → **30 selected** by SelectKBest
- **Split**: 80% training (26,048 rows) / 20% test (6,513 rows), stratified (random_state=42)
- **Target**: income >50K (coded as 1) or <=50K (coded as 0); ~76% <=50K, ~24% >50K (imbalanced)

## Primary Metric

**Precision** — business goal: minimize wasted outreach on low earners.

| Day | Baseline Precision |
|-----|-------------------|
| Day 1 (majority) | 0.0000 |
| Day 1 (rule baseline) | 0.4844 |
| Day 2 (Logistic Regression) | 0.7428 |
| Day 3 (HGB CV) | 0.7758 |
| **Day 4 (HGB tuned + calibrated)** | **0.9695** |
| **Day 5 (final, untouched test)** | **0.9695** |

## Week 1 Workflow Summary

### Day 1 — Baseline Models & Reproducibility
- Problem definition, EDA on raw data, stratified train/test splits
- Baselines: majority classifier (0% precision), rule-based (48.44% precision)
- Error analysis: identified 6 issues to fix (skewed capital-gain, native-country, redundant columns)
- Reproducibility: fixed random states, documented library versions
- **Deliverables**: `day1-task-soln.ipynb`, `day1-summary.pdf`, `eda_visualizations.png`, `eda_summary_table.csv`

### Day 2 — First Supervised Models
- Built ColumnTransformer pipeline (median impute + StandardScaler for numeric; most-frequent impute + OneHotEncoder for categorical)
- Trained Logistic Regression and Decision Tree on training set only
- Evaluated on locked hold-out test set
- LR won with Precision 0.7428, ROC AUC 0.9058; Tree overfit (train 0.9999 vs test 0.8186)
- Interpretability: LR coefficients revealed key drivers (capital-gain +2.26, Married-civ-spouse +1.54)
- **Deliverables**: `day2-soln.ipynb`, `day2-writeup.pdf`, `lr_pipeline.pkl`, `tree_pipeline.pkl`, `model_comparison.csv`

### Day 3 — Feature Engineering & Cross-Validation
- Created 7 engineered features based on domain knowledge
- Rebuilt pipeline with `FunctionTransformer(engineer_features)`
- 5-fold Stratified CV compared 3 models: **HGB wins** (Precision 0.7758 ± 0.0073)
- Wilcoxon signed-rank test: HGB won all 5 folds unanimously (p=0.0625)
- Feature selection: SelectKBest(mutual_info_classif, k=30) — negligible precision drop
- **Deliverables**: `day3-soln.ipynb`, `day3-writeup.pdf`, `notes.md`

### Day 4 — Model Tuning, Regularization & Calibration
- Hyperparameter search: `RandomizedSearchCV` (50 iterations, 5-fold CV)
- **Winner**: HistGradientBoosting (learning_rate=0.01432, max_iter=127, max_depth=10)
- Diagnostics: learning curves confirmed good fit (train-val gap 0.0389)
- Calibration: Isotonic regression improved Brier 0.0949 → 0.0918
- Threshold tuning: optimal threshold = 0.832, precision 0.9695
- Saved production pipeline and threshold info
- **Deliverables**: `day4-soln.ipynb`, `day4-tuning-report.pdf`, `day4-final-pipeline.joblib`, `day4-threshold-info.json`, `day4-best-{hgb,rf,lr}.joblib`, `day4-search-results.joblib`, `day4-*.png` (6 plots)

### Day 5 — Production-Ready ML Project
- Final validation on untouched test set (confirmed no leakage, precision 0.9695)
- Error analysis: confusion matrix (TP=476, FP=15, FN=1092, TN=4930), business cost analysis, subgroup analysis
- Feature importance via permutation importance: marital_status and capital_gain are top features
- Production inference: loaded pipeline, tested on 10 new examples, all automated
- Documentation: comprehensive README.md, project report PDF, requirements.txt, notes.md
- **Deliverables**: `final_model.joblib`, `day5-final-report.pdf`, `day5-feature-importance.png`, `day5-confusion-matrix.png`, `README.md`, `requirements.txt`, `notes.md`

## Final Model Architecture

```
Input (14 raw columns)
    │
    ▼
┌─────────────────────────┐
│ engineer_features()     │  ← adds 7 engineered columns (21 total)
│ (FunctionTransformer)   │
└──────────┬──────────────┘
           ▼
┌─────────────────────────┐
│ SimpleImputer(median)   │  ← numeric imputation
│ StandardScaler()        │  ← numeric scaling
└──────────┬──────────────┘
           ▼
┌─────────────────────────┐
│ SimpleImputer(most_freq)│  ← categorical imputation
│ OneHotEncoder()         │  ← categorical encoding (~122 features)
└──────────┬──────────────┘
           ▼
┌─────────────────────────┐
│ SelectKBest(k=30)       │  ← feature selection (mutual_info_classif)
└──────────┬──────────────┘
           ▼
┌─────────────────────────┐
│ HistGradientBoosting    │  ← tuned classifier
│ Classifier              │
└─────────────────────────┘
           │
           ▼
    predict_proba() → threshold 0.832 → final prediction
```

## Final Performance Summary

| Metric | Value |
|--------|-------|
| Precision | **0.9695** |
| Recall | 0.3036 |
| F1 Score | 0.4624 |
| Specificity | 0.9970 |
| Brier Score | 0.0918 |
| ROC AUC | 0.9213 |
| Optimal Threshold | 0.832 |

**Business Impact**: At threshold 0.832, only 15 false alarms (vs 303 at default threshold) — 96.95% of people we contact truly earn >$50K.

## Key Technical Lessons

1. **Pickling**: `FunctionTransformer` requires the function to be defined at module level before `joblib.load()`
2. **Column naming**: Pipeline expects `marital_status` (underscore), not `marital status` (space)
3. **HGB compatibility**: Needs `sparse_output=False` in OneHotEncoder (dense matrices required)
4. **Calibration ≠ Prediction**: Saved pipeline is raw (uncalibrated) but threshold was from calibrated probabilities
5. **Reproducibility**: All `random_state=42`, pinned library versions in `requirements.txt`
6. **Feature importance**: Permutation importance used instead of `feature_importances_` (HGB doesn't have it in sklearn 1.6.1)
7. **Unicode in PDFs**: fpdf2 doesn't support Unicode — all PDF text must be ASCII-only

## Files & Directory Structure

```
week-1/
├── README.md                          ← This file (Week 1 overview)
├── day-1/
│   ├── day1-task-soln.ipynb
│   ├── day1-task-statement.txt
│   ├── day1-summary.pdf
│   ├── eda_visualizations.png
│   ├── eda_summary_table.csv
│   ├── README.md
│   └── notes.md
├── day-2/
│   ├── day2-soln.ipynb
│   ├── day2-task-statement.txt
│   ├── day2-writeup.pdf
│   ├── lr_pipeline.pkl
│   ├── tree_pipeline.pkl
│   ├── model_comparison.csv
│   ├── README.md
│   └── notes.md
├── day-3/
│   ├── day3-soln.ipynb
│   ├── day3-task-statement.txt
│   ├── day3-writeup.pdf
│   ├── README.md
│   └── notes.md
├── day-4/
│   ├── day4-soln.ipynb
│   ├── day4-task-statement.txt         (empty)
│   ├── day4-tuning-report.pdf
│   ├── day4-final-pipeline.joblib
│   ├── day4-threshold-info.json
│   ├── day4-best-histgradientboosting.joblib
│   ├── day4-best-logisticregression.joblib
│   ├── day4-best-randomforest.joblib
│   ├── day4-search-results.joblib
│   ├── day4-learning-curve.png
│   ├── day4-validation-curves.png
│   ├── day4-calibration-plot.png
│   ├── day4-calibration-comparison.png
│   ├── day4-threshold-tuning.png
│   ├── README.md
│   └── notes.md
└── day-5/
    ├── day5-soln.ipynb
    ├── day5-task-statement.txt
    ├── day5-final-report.pdf
    ├── final_model.joblib
    ├── day5-feature-importance.png
    ├── day5-confusion-matrix.png
    ├── README.md
    ├── notes.md
    └── requirements.txt
```

## Python/Library Versions

| Library | Version |
|---------|---------|
| scikit-learn | 1.6.1 |
| pandas | 2.3.3 |
| numpy | 2.1.1 |
| joblib | 1.5.2 |
| scipy | 1.15.2 |
| matplotlib | 3.9.2 |
| seaborn | 0.13.2 |
| fpdf2 | 2.8.7 |

## How to Reproduce

1. Install dependencies: `pip install -r week-1/day-5/requirements.txt`
2. Open `day4-soln.ipynb` or `day5-soln.ipynb` in Jupyter
3. Run all cells in order
4. All `random_state=42` — results are reproducible across runs
5. Expected final precision: 0.9695 at threshold 0.832

## How to Run Inference

```python
import joblib, json, pandas as pd
pipeline = joblib.load('final_model.joblib')
with open('day4-threshold-info.json') as f:
    threshold_info = json.load(f)
OPTIMAL_THRESHOLD = threshold_info['optimal_threshold']
new_data = pd.DataFrame([{...}])  # 14 columns as training
probability = pipeline.predict_proba(new_data)[0, 1]
prediction = (probability >= OPTIMAL_THRESHOLD).astype(int)
```

**⚠️ Define `engineer_features()` at module level before `joblib.load()` (pickling requirement).**

## Status by Day

| Day | Status | Deliverables Complete |
|-----|--------|----------------------|
| Day 1 | ✅ Complete | 5/5 |
| Day 2 | ✅ Complete | 5/5 |
| Day 3 | ✅ Complete | 5/5 |
| Day 4 | ✅ Complete | 5/5 |
| Day 5 | ✅ Complete | 6/6 |
| **Week 1** | **✅ COMPLETE** | **26/26** |
