# Week 1 — Day 2: First Supervised Models

## Date
Sep 2, 2026

## Task
Build first real supervised models (Logistic Regression + Decision Tree)
with proper preprocessing pipelines, evaluate on hold-out test, and
select candidate model(s) for Day 3.

## Summary
Built a ColumnTransformer pipeline (median impute + StandardScaler for
numeric; most-frequent impute + OneHotEncoder for categorical), trained
Logistic Regression and Decision Tree on the training set only, evaluated
on the locked hold-out test, and checked interpretability of both.

## Progress
- [x] Task 1: Preprocessing Plan & Implementation (ColumnTransformer)
- [x] Task 2: Train Logistic Regression + Decision Tree in pipelines
- [x] Task 3: Evaluate on hold-out test (metrics, ROC/PR curves, confusion matrices)
- [x] Task 4: Interpretability (LR coefficients, tree depth/splits)
- [x] Task 5: Write-Up & Model Selection for Day 3

## Key Results
| Model | Accuracy | Precision | Recall | F1 | ROC AUC | PR AUC |
|-------|----------|-----------|--------|----|---------|--------|
| Day 1: Rule baseline (edu>=13) | 0.7530 | 0.4844 | 0.4970 | 0.4906 | 0.6653 | 0.3611 |
| **Logistic Regression** | **0.8542** | **0.7428** | 0.5979 | **0.6626** | **0.9058** | **0.7671** |
| Decision Tree (default) | 0.8186 | 0.6167 | 0.6394 | 0.6279 | 0.7574 | 0.4808 |

Confusion matrices:
- LR: `[[6947  484] [940 1398]]` — FN (940) > FP (484), misses earners more than over-predicts
- Tree: `[[6502  929] [843 1495]]` — FP (929) > FN (843), over-predicts positive class

## Interpretability
- **LR drivers:** positive — capital-gain (+2.26), Married-civ-spouse (+1.54),
  Exec-managerial (+0.82), education-num (+0.72). Negative — Priv-house-serv (-1.46),
  Never-married (-1.29), sex_Female (-1.03, dataset bias).
- **Tree:** depth 72, 5,668 leaves; train 0.9999 vs test 0.8186 = 0.18 overfit gap.
  Top splits (married → capital-gain → education) are sensible logic.

## Chosen Model for Day 3
- Model selected: **Logistic Regression**
- Why: highest precision (0.7428 vs 0.6167 tree, 0.4844 baseline) — aligned with
  business goal of avoiding wasted outreach; also best ROC AUC (0.906) and PR AUC (0.767),
  fully interpretable. Tree kept as secondary candidate after fixing overfitting.

## Preprocessing Changes Planned for Tomorrow
1. Drop `fnlwgt` (census sampling weight, not a real predictor)
2. `native-country`: collapse 41 categories into US vs Other
3. Drop redundant `education` column (keep `education-num`)
4. `marital-status`: collapse to Married vs Not-Married
5. `capital-gain`/`capital-loss`: log-transform or bin (dominated by 0)
6. `hours-per-week`: cap at 95th percentile

## Files
- `day2-task-statement.txt` — task instructions
- `day2-soln.ipynb` — notebook (all 5 tasks)
- `day2-writeup.pdf` — 1-2 page write-up (deliverable)
- `model_comparison.csv` — comparison table
- `notes.md` — personal revision notes (gitignored)
- `README.md` — this file