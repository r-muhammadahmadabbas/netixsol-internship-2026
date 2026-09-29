"""
Week 3 Day 2: Prediction Models
Match Winner + Top Player models with baselines
"""
import pandas as pd
import numpy as np
import os
import sys
import joblib
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, brier_score_loss, mean_absolute_error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load data
data_path = r"C:\Internship\Netixsol\week-3\day-1"
feature_table = pd.read_csv(os.path.join(data_path, "feature_table.csv"))
train = pd.read_csv(os.path.join(data_path, "train.csv"))
val = pd.read_csv(os.path.join(data_path, "val.csv"))
test = pd.read_csv(os.path.join(data_path, "test.csv"))

print(f"Train: {len(train)}, Val: {len(val)}, Test: {len(test)}")

# Features for match winner model
FEATURES = [
    'win_streak', 'avg_score_3', 'avg_conceded_3', 'avg_margin_3',
    'avg_score_5', 'avg_conceded_5', 'form_5',
    'h2h_win_rate', 'h2h_avg_margin', 'h2h_meetings',
    'days_rest', 'is_home', 'venue_experience'
]

# Prepare data
X_train = train[FEATURES].fillna(0)
y_train = train['home_win']
X_val = val[FEATURES].fillna(0)
y_val = val['home_win']
X_test = test[FEATURES].fillna(0)
y_test = test['home_win']

print(f"Features: {len(FEATURES)}")
print(f"Target distribution - Train: {y_train.mean():.1%}, Test: {y_test.mean():.1%}")

# ============================================================================
# BASELINE MODELS
# ============================================================================
print("\n" + "=" * 60)
print("BASELINE MODELS")
print("=" * 60)

# Baseline 1: Always predict home win
baseline1_pred = np.ones(len(y_test))
baseline1_acc = accuracy_score(y_test, baseline1_pred)
print(f"Baseline 1 (Always Home Win): Accuracy = {baseline1_acc:.1%}")

# Baseline 2: Predict based on form_5 (higher form wins)
baseline2_pred = (test['form_5'] > 0.5).astype(int)
baseline2_acc = accuracy_score(y_test, baseline2_pred)
print(f"Baseline 2 (Form-based): Accuracy = {baseline2_acc:.1%}")

# ============================================================================
# MATCH WINNER MODEL
# ============================================================================
print("\n" + "=" * 60)
print("MATCH WINNER MODEL")
print("=" * 60)

# Model 1: Logistic Regression
lr_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('lr', LogisticRegression(max_iter=1000, random_state=42))
])
lr_pipeline.fit(X_train, y_train)
lr_pred = lr_pipeline.predict(X_test)
lr_prob = lr_pipeline.predict_proba(X_test)[:, 1]

print(f"\nLogistic Regression:")
print(f"  Accuracy: {accuracy_score(y_test, lr_pred):.1%}")
print(f"  F1 Score: {f1_score(y_test, lr_pred):.3f}")
print(f"  ROC AUC: {roc_auc_score(y_test, lr_prob):.3f}")
print(f"  Brier Score: {brier_score_loss(y_test, lr_prob):.3f}")

# Model 2: Gradient Boosting
gb_model = GradientBoostingClassifier(
    n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42
)
gb_model.fit(X_train, y_train)
gb_pred = gb_model.predict(X_test)
gb_prob = gb_model.predict_proba(X_test)[:, 1]

print(f"\nGradient Boosting:")
print(f"  Accuracy: {accuracy_score(y_test, gb_pred):.1%}")
print(f"  F1 Score: {f1_score(y_test, gb_pred):.3f}")
print(f"  ROC AUC: {roc_auc_score(y_test, gb_prob):.3f}")
print(f"  Brier Score: {brier_score_loss(y_test, gb_prob):.3f}")

# Feature importance
importance = pd.DataFrame({
    'feature': FEATURES,
    'importance': gb_model.feature_importances_
}).sort_values('importance', ascending=False)

print(f"\nTop 5 Features:")
for _, row in importance.head(5).iterrows():
    print(f"  {row['feature']}: {row['importance']:.3f}")

# Save best model
joblib.dump(gb_model, os.path.join(data_path, "match_winner_model.joblib"))
print(f"\nModel saved: match_winner_model.joblib")

# ============================================================================
# TOP PLAYER MODEL
# ============================================================================
print("\n" + "=" * 60)
print("TOP PLAYER MODEL")
print("=" * 60)

# Load player data
player_game = pd.read_csv(os.path.join(data_path, "player_game_eda.csv"))

# Features for player model
PLAYER_FEATURES = ['year', 'career_game_count', 'fantasy_points', 'score', 'margin']

# Create target: top performer in each match (top 20% fantasy points)
player_game['is_top'] = (player_game['fantasy_points'] > player_game['fantasy_points'].quantile(0.8)).astype(int)

X_player = player_game[PLAYER_FEATURES].fillna(0)
y_player = player_game['is_top']

# Split by time
split_idx = int(len(player_game) * 0.8)
X_p_train = X_player.iloc[:split_idx]
y_p_train = y_player.iloc[:split_idx]
X_p_test = X_player.iloc[split_idx:]
y_p_test = y_player.iloc[split_idx:]

# Train model
player_model = GradientBoostingClassifier(n_estimators=50, max_depth=3, random_state=42)
player_model.fit(X_p_train, y_p_train)
player_pred = player_model.predict(X_p_test)
player_prob = player_model.predict_proba(X_p_test)[:, 1]

print(f"Top Player Model:")
print(f"  Accuracy: {accuracy_score(y_p_test, player_pred):.1%}")
print(f"  ROC AUC: {roc_auc_score(y_p_test, player_prob):.3f}")

# Baseline: predict based on season average
baseline_player_pred = (X_p_test['fantasy_points'] > X_p_test['fantasy_points'].median()).astype(int)
print(f"  Baseline (median): {accuracy_score(y_p_test, baseline_player_pred):.1%}")

joblib.dump(player_model, os.path.join(data_path, "top_player_model.joblib"))
print(f"Model saved: top_player_model.joblib")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Match Winner - Baseline: {baseline1_acc:.1%} | GB Model: {accuracy_score(y_test, gb_pred):.1%}")
print(f"Top Player - Baseline: {accuracy_score(y_test, baseline_player_pred):.1%} | GB Model: {accuracy_score(y_p_test, player_pred):.1%}")
print(f"\nModels beat baselines: {accuracy_score(y_test, gb_pred) > baseline1_acc}")
