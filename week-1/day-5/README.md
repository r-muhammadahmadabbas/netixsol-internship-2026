# Week 1 — Final Machine Learning Project: UCI Adult (Census Income) Prediction

## Status: COMPLETE

## Project Objective

Build a machine learning model to predict whether a person earns more than $50,000 per year based on demographic and employment data from the UCI Adult Census dataset. The primary business goal is to **maximize precision** — minimize wasted outreach by only contacting people who are very likely high earners.

## Dataset Description

- **Source**: UCI Machine Learning Repository (Adult/Census Income dataset)
- **URL**: https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data
- **Total rows**: 48,842 (after dropping missing values)
- **Features**: 14 raw columns
  - Numeric: age, fnlwgt, education_num, capital_gain, capital_loss, hours_per_week
  - Categorical: workclass, education, marital_status, occupation, relationship, race, sex, native_country
- **Engineered features**: 7 additional columns created via `engineer_features()`
  - log_capital_gain, has_capital_gain, has_capital_loss, age_group, hours_category, higher_ed, edu_hours_interaction
- **Total columns after engineering**: 21 (14 original + 7 engineered)
- **Preprocessing output**: ~122 features after one-hot encoding
- **Final selected features**: 30 (selected by SelectKBest with mutual_info_classif)
- **Split**: 80% training (26,048 rows) / 20% test (6,513 rows), stratified (random_state=42)

## Target Variable

- **Name**: income
- **Values**: >50K (coded as 1) or <=50K (coded as 0)
- **Class distribution**: ~76% <=50K, ~24% >50K (imbalanced)
- **Encoding**: `(df['income'] == '>50K').astype(int)` — 1 if income exceeds $50K, else 0

## Feature Engineering (Day 3)

Seven engineered features created based on domain knowledge:

| # | Feature | Type | Rationale |
|---|---------|------|-----------|
| 1 | `log_capital_gain` | numeric | Compresses extremely skewed capital_gain range |
| 2 | `has_capital_gain` | binary | Presence of any capital gain is informative |
| 3 | `has_capital_loss` | binary | Capital losses less common among high earners |
| 4 | `age_group` | categorical | Life-cycle income pattern (young, peak, retired) |
| 5 | `hours_category` | categorical | Part-time vs full-time vs overtime |
| 6 | `higher_ed` | binary | Bachelor's degree or above = higher earning potential |
| 7 | `edu_hours_interaction` | numeric | Education * hours captures synergy of both factors |

## Preprocessing Steps (Pipeline)

The entire pipeline automates all preprocessing:

1. **Feature Engineering**: `FunctionTransformer(engineer_features)` adds 7 columns
2. **Numeric Imputation**: `SimpleImputer(strategy='median')` fills missing values
3. **Numeric Scaling**: `StandardScaler()` standardizes to mean=0, std=1
4. **Categorical Imputation**: `SimpleImputer(strategy='most_frequent')` fills missing categories
5. **Categorical Encoding**: `OneHotEncoder(handle_unknown='ignore', sparse_output=False)` creates binary columns
6. **Feature Selection**: `SelectKBest(mutual_info_classif, k=30)` keeps top 30 features
7. **Model**: `HistGradientBoostingClassifier` with tuned hyperparameters

**Note**: `OneHotEncoder(sparse_output=False)` is required because HistGradientBoostingClassifier needs dense matrices.

## Models Tested

| Model | Type | CV Precision | Notes |
|-------|------|-------------|-------|
| Logistic Regression | Linear | 0.7666 | Baseline; L1 regularization with C=0.00108 |
| Random Forest | Ensemble | 0.8018 | 189 trees, max_depth=5, max_features=log2 |
| HistGradientBoosting | Boosted Trees | **0.8025** | **WINNER** |

## Hyperparameter Tuning Approach (Day 4)

- **Method**: `RandomizedSearchCV` with 5-fold Stratified CV, optimizing for precision
- **Budget**: 50 iterations for LR and HGB, 30 for RF, totaling ~30 minutes
- **Best HGB hyperparameters**: learning_rate=0.01432, max_iter=127, max_depth=10, l2_regularization=0.0152, min_samples_leaf=16

## Selected Final Model

**Model**: HistGradientBoostingClassifier (tuned + calibrated + threshold-tuned)

**Pipeline structure**: engineer → preprocessor → select → model

**Calibration**: Isotonic regression (5-fold CV) improved Brier score from 0.0949 to 0.0918

**Threshold**: 0.832 (chosen to maximize precision while maintaining recall >= 0.30)

## Final Test Performance (Hold-out Test Set)

| Metric | Value | Interpretation |
|--------|-------|----------------|
| **Precision** | **0.9695** | Of every 100 people flagged, 97 are truly high earners |
| **Recall** | 0.3036 | Of all real high earners, we catch 30% |
| **F1 Score** | 0.4624 | Harmonic balance of precision and recall |
| **Specificity** | 0.9970 | Of every 100 low earners, we correctly leave 99 alone |
| **Brier Score** | 0.0918 | Well-calibrated probabilities (perfect=0, random=0.25) |
| **ROC AUC** | 0.9213 | Strong discriminative ability |
| **Optimal Threshold** | 0.832 | Maximizes precision with recall >= 0.30 |

**Confusion Matrix at threshold 0.832**: TP=476, FP=15, FN=1092, TN=4930

## Important Features (Day 5 Feature Importance)

Top features by permutation importance:

| Rank | Feature | Importance | Business Meaning |
|------|---------|-----------|------------------|
| 1 | marital_status | 0.0524 | Strong proxy for household income |
| 2 | capital_gain | 0.0502 | Direct wealth signal |
| 3 | education_num | 0.0352 | More education = higher earning potential |
| 4 | age | 0.0222 | Career peak income in middle age |
| 5 | capital_loss | 0.0132 | Capital losses less common among high earners |
| 6 | hours_per_week | 0.0094 | Longer hours correlate with higher pay |
| 7 | sex | 0.0042 | Gender pay gap present in dataset |

**Surprising finding**: `fnlwgt` (sampling weight) has NEGATIVE importance (-0.0072) — the model correctly avoided noise. workclass, relationship, native_country had near-zero importance.

## Known Limitations

1. **Low recall (0.3036)**: Model misses ~70% of true high earners
2. **Pipeline is raw model**: Threshold was derived from calibrated probabilities but the saved pipeline is uncalibrated
3. **Pickling requirement**: `engineer_features` must be defined before `joblib.load()` in new sessions
4. **Column naming quirk**: Pipeline expects `marital_status` (underscore), not `marital status` (space)
5. **Single dataset**: Only UCI Adult dataset tested
6. **No subgroup-specific thresholds**: Single threshold applied globally
7. **fnlwgt noise**: Sampling weight survived feature selection

## How to Reproduce Training

1. Install dependencies: `pip install -r requirements.txt`
2. Open `day5-soln.ipynb` in Jupyter
3. Run all cells in order (Tasks 1-4)
4. All `random_state=42` — results are reproducible across runs
5. Expected final precision: 0.9695 at threshold 0.832

## How to Run Inference

```python
import joblib
import json
import pandas as pd

# Load pipeline and threshold
pipeline = joblib.load('final_model.joblib')
with open('day4-threshold-info.json') as f:
    threshold_info = json.load(f)
OPTIMAL_THRESHOLD = threshold_info['optimal_threshold']

# Create new data (same 14 columns as training)
new_data = pd.DataFrame([{
    'age': 35, 'workclass': 'Private', 'fnlwgt': 200000,
    'education': 'Bachelors', 'education_num': 13,
    'marital_status': 'Married-civ-spouse',
    'occupation': 'Exec-managerial', 'relationship': 'Husband',
    'race': 'White', 'sex': 'Male',
    'capital_gain': 5000, 'capital_loss': 0,
    'hours_per_week': 50, 'native_country': 'United-States'
}])

# Get prediction
probability = pipeline.predict_proba(new_data)[0, 1]
prediction = (probability >= OPTIMAL_THRESHOLD).astype(int)

print(f"Probability: {probability:.4f}")
print(f"Threshold: {OPTIMAL_THRESHOLD:.3f}")
print(f"Prediction: {'>50K' if prediction else '<=50K'}")
```

Note: Define `engineer_features()` at module level before `joblib.load()` (required for pickling). The pipeline handles ALL preprocessing automatically.

## Week 1 Workflow Summary

- **Day 1**: Baseline models + Reproducibility
- **Day 2**: Hyperparameter search (HGB wins)
- **Day 3**: Feature engineering + Cross-validation
- **Day 4**: Calibration + Threshold tuning (precision 0.9695)
- **Day 5**: Final validation + Error analysis + Feature importance + Inference + Documentation

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

## Key Files

| File | Purpose |
|------|---------|
| `final_model.joblib` | Complete trained pipeline (engineer → preprocess → select → model) |
| `day4-threshold-info.json` | Optimal threshold (0.832) + final metrics |
| `day5-final-report.pdf` | 4-page final project report |
| `day5-feature-importance.png` | Feature importance visualization |
| `day5-confusion-matrix.png` | Confusion matrix heatmap |
| `day4-tuning-report.pdf` | Hyperparameter tuning summary |
| `requirements.txt` | Pinned library versions |
| `notes.md` | Detailed concept explanations for Tasks 3, 4, 5 |
