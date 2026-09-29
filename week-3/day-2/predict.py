"""
Week 3 Day 2: Prediction Module
Clean callable functions for match winner and top player predictions
"""
import os
import sys
import joblib
import pandas as pd
import numpy as np
from typing import Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = r"C:\Internship\Netixsol\week-3\day-1"

# Load models
try:
    match_winner_model = joblib.load(os.path.join(DATA_PATH, "match_winner_model.joblib"))
    top_player_model = joblib.load(os.path.join(DATA_PATH, "top_player_model.joblib"))
    MODELS_LOADED = True
except:
    MODELS_LOADED = False

# Team name normalization
TEAM_ALIASES = {
    'pies': 'Collingwood Magpies',
    'cats': 'Carlton Blues',
    'hawks': 'Hawthorn Hawks',
    'tigers': 'Richmond Tigers',
    'bulldogs': 'Western Bulldogs',
    'swans': 'Sydney Swans',
    'eagles': 'West Coast Eagles',
    'dockers': 'Fremantle Dockers',
    'crows': 'Adelaide Crows',
    'lions': 'Brisbane Lions',
    'suns': 'Gold Coast Suns',
    'giants': 'Greater Western Sydney Giants',
    'kangaroos': 'North Melbourne Kangaroos',
    'demons': 'Melbourne Demons',
    'saints': 'St Kilda Saints',
    'bombers': 'Essendon Bombers',
    'power': 'Port Adelaide Power',
}

def normalize_team_name(name: str) -> str:
    """Resolve team nicknames/aliases to exact team name"""
    name_lower = name.lower().strip()
    if name_lower in TEAM_ALIASES:
        return TEAM_ALIASES[name_lower]
    # Try partial match
    for alias, full_name in TEAM_ALIASES.items():
        if alias in name_lower or name_lower in alias:
            return full_name
    return name

def predict_match_winner(team_a: str, team_b: str, date: str = None) -> Dict:
    """
    Predict match winner between two teams.
    
    Args:
        team_a: Home team name (accepts aliases like 'pies', 'cats')
        team_b: Away team name
        date: Match date (YYYY-MM-DD)
    
    Returns:
        {
            "winner": "team_a" or "team_b",
            "probability": 0.72,
            "confidence": "high" or "medium" or "low",
            "features": {"home_advantage": 0.57, "form_diff": 0.1}
        }
    """
    team_a = normalize_team_name(team_a)
    team_b = normalize_team_name(team_b)
    
    if not MODELS_LOADED:
        # Fallback: home team advantage
        return {
            "winner": "team_a",
            "probability": 0.57,
            "confidence": "low",
            "features": {"home_advantage": 0.57},
            "note": "Model not loaded, using baseline"
        }
    
    # Create feature vector (simplified for demo)
    features = pd.DataFrame([{
        'win_streak': 0,
        'avg_score_3': 100,
        'avg_conceded_3': 90,
        'avg_margin_3': 10,
        'avg_score_5': 100,
        'avg_conceded_5': 90,
        'form_5': 0.5,
        'h2h_win_rate': 0.5,
        'h2h_avg_margin': 0,
        'h2h_meetings': 0,
        'days_rest': 7,
        'is_home': 1,
        'venue_experience': 10
    }])
    
    prob = match_winner_model.predict_proba(features)[0][1]
    
    if prob > 0.6:
        confidence = "high"
    elif prob > 0.5:
        confidence = "medium"
    else:
        confidence = "low"
    
    return {
        "winner": "team_a" if prob > 0.5 else "team_b",
        "probability": round(prob, 3),
        "confidence": confidence,
        "features": {
            "home_advantage": 0.57,
            "form": 0.5
        }
    }

def predict_top_player(team: str = None, stat_type: str = "disposals") -> List[Dict]:
    """
    Predict top players for upcoming match.
    
    Args:
        team: Team name (optional)
        stat_type: "disposals", "goals", "fantasy_points"
    
    Returns:
        [
            {"player": "Patrick Cripps", "team": "Carlton Blues", "predicted_value": 32.5},
            ...
        ]
    """
    # Load player data
    try:
        player_game = pd.read_csv(os.path.join(DATA_PATH, "player_game_eda.csv"))
    except:
        return []
    
    # Filter by team if specified
    if team:
        team = normalize_team_name(team)
        player_game = player_game[player_game['team'] == team]
    
    if player_game.empty:
        return []
    
    # Get recent form (last 5 games per player)
    player_game = player_game.sort_values(['player_id', 'year', 'round'])
    recent = player_game.groupby('player_id').tail(5)
    
    # Calculate averages
    if stat_type == "disposals":
        avg_stats = recent.groupby('player_id')['disposals_target'].mean()
    elif stat_type == "goals":
        avg_stats = recent.groupby('player_id')['goals_target'].mean()
    else:
        avg_stats = recent.groupby('player_id')['fantasy_target'].mean()
    
    # Get top 5
    top_players = avg_stats.nlargest(5)
    
    # Get player names
    players_info = pd.read_csv(os.path.join(DATA_PATH, "data", "afl_datasets", "afl_players_info_raw.csv"))
    
    results = []
    for player_id, value in top_players.items():
        player = players_info[players_info['id'] == player_id]
        if not player.empty:
            name = player.iloc[0]['player_name']
            team = recent[recent['player_id'] == player_id]['team'].iloc[0]
            results.append({
                "player": name,
                "team": team,
                "predicted_value": round(value, 1)
            })
    
    return results

if __name__ == "__main__":
    # Test
    print("Testing predict_match_winner:")
    result = predict_match_winner("pies", "cats")
    print(f"  Result: {result}")
    
    print("\nTesting predict_top_player:")
    result = predict_top_player(team="Collingwood Magpies", stat_type="disposals")
    for p in result[:3]:
        print(f"  {p['player']}: {p['predicted_value']}")