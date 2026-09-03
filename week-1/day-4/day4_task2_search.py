# ═══════════════════════════════════════════════════════════════
# TASK 2: HYPERPARAMETER SEARCH (RANDOMIZED SEARCH CV) - OPTIMIZED
# ═══════════════════════════════════════════════════════════════

# ─── SECTION 1: IMPORTS FOR HYPERPARAMETER SEARCH ───
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold
from scipy.stats import loguniform, randint, uniform
import numpy as np
import pandas as pd
import time
import joblib
import warnings
warnings.filterwarnings('ignore')

# ─── SECTION 2: REUSE TASK 1 PIPELINES & DATA ───
# This assumes you've already run Task 1 and have:
# - pipelines dict with 3 pipelines
# - X_train, X_test, y_train, y_test
# - RANDOM_SEED = 42
# - engineer_features function
# - preprocessor, selector, etc.

# If running standalone, you'd need to re-run Task 1 setup first.
# For now, assuming Task 1 variables exist in your notebook.

# ─── SECTION 2: DEFINE CV STRATEGY (SAME FOR ALL SEARCHES) ───
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_SEED)

# ─── SECTION 3: DEFINE HYPERPARAMETER SEARCH SPACES ───

# ─── 3A: LOGISTIC REGRESSION SEARCH SPACE (unchanged - fast) ───
param_dist_lr = {
    'model__penalty': ['l1', 'l2'],
    'model__C': loguniform(1e-3, 1e3),
    'model__solver': ['liblinear'],
    'model__max_iter': [1000],
}

# ─── 3B: RANDOM FOREST SEARCH SPACE (OPTIMIZED FOR SPEED) ───
# Reduced ranges for faster search - RF rarely beats HGB anyway
param_dist_rf = {
    'model__n_estimators': randint(100, 301),        # 100-300 (was 100-500)
    'model__max_depth': [5, 10, 15, 20, None],
    'model__min_samples_leaf': randint(1, 9),
    'model__max_features': ['sqrt', 'log2', 0.5],    # 3 options (was 4)
    'model__min_samples_split': randint(2, 11),
}

# ─── 3C: HISTGRADIENTBOOSTING SEARCH SPACE (unchanged - fast) ───
param_dist_hgb = {
    'model__learning_rate': loguniform(0.01, 0.3),
    'model__max_iter': randint(100, 501),
    'model__max_depth': [3, 5, 7, 10, None],
    'model__l2_regularization': loguniform(1e-3, 10),
    'model__min_samples_leaf': randint(5, 21),
    'model__max_leaf_nodes': [15, 31, 63, None],
}

# ─── SECTION 4: SEARCH CONFIGURATIONS ───

# Base config (shared by LR and HGB)
BASE_SEARCH_CONFIG = {
    'cv': cv,
    'scoring': 'precision',
    'n_jobs': -1,
    'random_state': RANDOM_SEED,
    'verbose': 1,
    'return_train_score': True,
    'error_score': np.nan,
}

# LR & HGB: 50 iterations (they're fast)
LR_HGB_CONFIG = {
    **BASE_SEARCH_CONFIG,
    'n_iter': 50,
    'verbose': 1,
    'return_train_score': True,
    'error_score': np.nan,
}

# RF: Reduced budget for speed (30 iterations, smaller space)
RF_CONFIG = {
    **BASE_SEARCH_CONFIG,
    'n_iter': 30,
    'verbose': 1,
    'return_train_score': True,
    'error_score': np.nan,
}

# ─── SECTION 4: CREATE SEARCH OBJECTS ───
search_lr = RandomizedSearchCV(
    estimator=pipelines['LogisticRegression'],
    param_distributions=param_dist_lr,
    **LR_HGB_CONFIG
)

search_rf = RandomizedSearchCV(
    estimator=pipelines['RandomForest'],
    param_distributions=param_dist_rf,
    **RF_CONFIG
)

search_hgb = RandomizedSearchCV(
    estimator=pipelines['HistGradientBoosting'],
    param_distributions=param_dist_hgb,
    **LR_HGB_CONFIG
)

# ─── SECTION 5: RUN ALL THREE SEARCHES ───
searches = {
    'LogisticRegression': search_lr,
    'RandomForest': search_rf,
    'HistGradientBoosting': search_hgb
}

search_results = {}

print("\n" + "="*70)
print("STARTING HYPERPARAMETER SEARCHES (OPTIMIZED)")
print("="*70)
print(f"CV: 5-fold Stratified (seed=42)")
print(f"LR & HGB: 50 iterations each | RF: 30 iterations (fast)")
print(f"Scoring: precision (primary metric)")
print(f"Parallel jobs: all cores (n_jobs=-1)")
print("="*70)

for name, search in searches.items():
    print(f"\n{'='*70}")
    print(f"SEARCHING: {name}")
    print(f"{'='*70}")
    
    start_time = time.time()
    search.fit(X_train, y_train)
    elapsed = time.time() - start_time
    
    search_results[name] = {
        'search': search,
        'best_params': search.best_params_,
        'best_score': search.best_score_,
        'best_estimator': search.best_estimator_,
        'cv_results': search.cv_results_,
        'time_seconds': elapsed
    }
    
    print(f"\n✅ {name} COMPLETE in {elapsed:.1f}s")
    print(f"   Best CV Precision: {search.best_score_:.4f}")
    print(f"   Best Params: {search.best_params_}")

# ─── SECTION 6: COMPARE RESULTS & SELECT BEST ───
print("\n" + "="*70)
print("HYPERPARAMETER SEARCH RESULTS SUMMARY")
print("="*70)

summary_rows = []
for name, result in search_results.items():
    summary_rows.append({
        'Model': name,
        'Best_CV_Precision': result['best_score'],
        'Best_Params': str(result['best_params']),
        'Time_Seconds': round(result['time_seconds'], 1)
    })

summary_df = pd.DataFrame(summary_rows)
print(summary_df.to_string(index=False))

# Select overall best model by CV precision
best_model_name = max(search_results.keys(), key=lambda k: search_results[k]['best_score'])
best_result = search_results[best_model_name]
best_pipeline = best_result['best_estimator']

print(f"\n🏆 OVERALL BEST MODEL: {best_model_name}")
print(f"   Best CV Precision: {best_result['best_score']:.4f}")
print(f"   Best Parameters: {best_result['best_params']}")

# ─── SECTION 7: DETAILED CV RESULTS ANALYSIS ───
print(f"\n📊 TOP 5 COMBINATIONS FOR {best_model_name}:")
cv_results = best_result['cv_results']

results_df = pd.DataFrame({
    'mean_precision': cv_results['mean_test_score'],
    'std_precision': cv_results['std_test_score'],
    'mean_train_precision': cv_results['mean_train_score'],
    'params': cv_results['params']
}).sort_values('mean_precision', ascending=False)

print(results_df.head(5)[['mean_precision', 'std_precision', 'mean_train_precision', 'params']].to_string(index=False))

# ─── SECTION 8: SAVE BEST PIPELINES & RESULTS ───
best_pipelines = {
    name: result['best_estimator'] 
    for name, result in search_results.items()
}

joblib.dump(search_results, 'day4-search-results.joblib')
print("\n💾 Saved search_results to 'day4-search-results.joblib'")

# Also save best pipelines individually
for name, pipe in best_pipelines.items():
    joblib.dump(pipe, f'day4-best-{name.lower().replace(" ", "-")}.joblib')

print("\n✅ TASK 2 COMPLETE — Ready for Task 3 (Learning Curves)")