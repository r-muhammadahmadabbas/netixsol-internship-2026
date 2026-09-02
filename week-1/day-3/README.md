# Day 3 — Feature Engineering & Cross-Validation

## Status: COMPLETE

### Overview
Day 3 focused on expanding the feature set with principled feature engineering and using cross-validation to compare models more reliably. The goal was to find features that materially improve performance and get statistically believable performance estimates before tuning.

### Tasks Completed

| Task | Description | Status |
|------|-------------|--------|
| **Task 1** | Created & justified 7 engineered features (age buckets, hours-per-week bins, capital gain/loss flags, higher-ed boolean, education×hours interaction). Mutual information scores computed for each. Feature dictionary maintained. | ✅ |
| **Task 2** | Rebuilt pipeline integrating engineered features via `FunctionTransformer`. Fixed bug where `engineer_features()` dropped original columns (now returns 21 cols: 14 original + 7 engineered). Fixed `OneHotEncoder sparse_output=True → False` for HGB compatibility. | ✅ |
| **Task 3** | 5-fold Stratified CV compared 3 models: LogisticRegression, RandomForest, HistGradientBoosting. **HGB wins** — Precision 0.7758 ± 0.0073, Recall 0.6526 ± 0.0102, F1 0.7089 ± 0.0078, ROC AUC 0.9255 ± 0.0025. Most stable model (lowest std). | ✅ |
| **Task 4** | Wilcoxon signed-rank test between HGB and LR on Precision. p = 0.0625 (n=5 power limit), but HGB won all 5 folds (unanimous direction). Practical significance: +3pp precision improvement meaningful for business goal. Feature importance extracted via tree-based importances and LR coefficients. | ✅ |
| **Task 5** | Feature selection with `SelectKBest(mutual_info_classif)`. LR comparison: All (122) → precision 0.7455; Top-30 → 0.7429 (negligible drop 0.0026). HGB All vs Top-30: 0.7758 → 0.7647 (drop 0.0112, 1.4% relative — acceptable). Top-30 selected features: `edu_hours_interaction`, `log_capital_gain`, `capital_gain`, `higher_ed`, `age_group_40-54`. | ✅ |

### Engineered Features (7 total)

| # | Feature | Type | MI Score | Why |
|---|---------|------|----------|-----|
| 1 | `log_capital_gain` | numeric | 0.0843 | Compresses skewed capital-gain range |
| 2 | `edu_hours_interaction` | numeric | 0.0829 | Combined effect: education + hours |
| 3 | `higher_ed` | binary | 0.0317 | College-degree flag vs no degree |
| 4 | `has_capital_gain` | binary | 0.0260 | Presence/absence of any gain |
| 4 | `age_group_40-54` | category | 0.0253 | Peak earning years (life-cycle) |
| 5 | `hours_category_50+` | category | 0.0230 | Overtime work correlates with income |
| 6 | `has_capital_loss` | binary | 0.0102 | Fewer people have capital losses |

### Key Results

- **HGB wins** on all 4 metrics (precision, recall, F1, ROC AUC) and is most stable
- **Wilcoxon test**: p=0.0625 (n=5 power limit), HGB won all 5 folds unanimously
- **Feature selection**: Top-30 retains 96% of All-feature precision for HGB (drop only 0.0112)
- **Recommended keep**: `log_capital_gain`, `edu_hours_interaction`, `higher_ed`, `age_group_40-54`, `capital_gain`, `education_num`, `hours_per_week`, `marital status`, `occupation`
- **Recommended drop**: `has_capital_gain` (redundant with `log_capital_gain`), `fnlwgt` (sampling weight), weak native-country bins

### Deliverables

- **Notebook**: `day3-soln.ipynb` — all 5 tasks with code and results
- **PDF write-up**: `day3-writeup.pdf` — 2-page summary with feature list, CV comparison, statistical test results, and feature recommendations
- **Notes**: `week-1/day-2/notes.md` — updated with entries 30–81 (algorithms, CV, ensembles, Wilcoxon, feature importance)

### How to Run

1. Open `day3-soln.ipynb` in Jupyter
2. Run all cells (5 tasks)
3. The PDF `day3-writeup.pdf` is generated from the notebook output
4. Review the feature recommendations for Day 4 hyperparameter tuning

### Next Steps (Day 4)

- Hyperparameter tuning on the winning model (HistGradientBoosting)
- Feature selection based on Day 3 results (keep: `log_capital_gain`, `edu_hours_interaction`, etc.; drop: `has_capital_gain`, `fnlwgt`)
- Evaluate on the hold-out test set for final performance measurement