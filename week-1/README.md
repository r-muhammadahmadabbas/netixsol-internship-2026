# Week 1 — Day 1: All 5 Tasks

## Dataset
UCI Adult (Census Income) — 48,842 samples, 15 features, target: income >50K (binary).

## Tasks Completed

### Task 1: Problem Definition & Success Metric
- Target: >50K = 1, <=50K = 0
- Class base rate: 23.93%
- Business objective: Maximize precision to avoid wasted outreach
- Primary metric: Precision

### Task 2: Data Load & Quick EDA
- Missing values in workclass (2,799), occupation (2,809), native-country (857) — filled with "Unknown"
- Key findings: capital-gain/loss heavily skewed, native-country 90% US, education has 16 categories
- Visualizations saved: eda_visualizations.png
- Summary table saved: eda_summary_table.csv

### Task 3: Reproducible Splits
- Train: 39,073 samples, Test: 9,769 samples (80/20 split)
- Stratified on target, random_state=42
- Both splits have 23.93% base rate

### Task 4: Baselines
| Model | Accuracy | Precision | Recall | F1 | ROC AUC | PR AUC |
|-------|----------|-----------|--------|----|---------|--------|
| Majority (always <=50K) | 0.7607 | 0.0000 | 0.0000 | 0.0000 | 0.5000 | 0.2393 |
| Rule (education-num >= 13) | 0.7530 | 0.4844 | 0.4970 | 0.4906 | 0.6653 | 0.3611 |

Rule-based baseline wins — it actually identifies positive cases. Real model needs F1 >= 0.60 to be useful.

### Task 5: Error Analysis
- False positives: 1,237 — mostly Bachelors+ in low-paying sectors, capital-gain=0
- False negatives: 1,176 — mostly no degree but high hours/week, some with capital-gain > 0

**6 issues to fix tomorrow:**
1. Capital-gain/loss: log transform or binning
2. Native-country: group US vs Other
3. Drop redundant education column (keep education-num)
4. Marital-status: group Married vs Not-Married
5. Occupation: group rare categories into Other
6. Hours-per-week: cap outliers at 95th percentile

**Primary metric for rest of week:** Precision (baseline = 48.4%, target >= 65%)

## Files
- `day1-task-soln.ipynb` — all 5 tasks in one notebook
- `eda_visualizations.png` — 6 plots (histograms + bar plots)
- `eda_summary_table.csv` — summary statistics
- `README.md` — this file