"""
Week 3 Day 3: Domain-Scoped AFL Chat Agent
Retrieval, guardrails, grounding, memory
"""
import os
import sys
import pandas as pd
from typing import List, Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = r"C:\Internship\Netixsol\week-3\day-1"

# ============================================================================
# RETRIEVAL TOOLS
# ============================================================================

def get_team_record(team_name: str, year: int = None) -> Dict:
    """Get team's win-loss record"""
    try:
        matches = pd.read_csv(os.path.join(DATA_PATH, "home_matches_eda.csv"))
        team_matches = matches[matches['team_name'] == team_name]
        if year:
            team_matches = team_matches[team_matches['year'] == year]
        
        wins = (team_matches['home_win'] == 1).sum()
        losses = (team_matches['home_win'] == 0).sum()
        total = wins + losses
        
        return {
            "team": team_name,
            "wins": int(wins),
            "losses": int(losses),
            "win_rate": round(wins / total, 2) if total > 0 else 0,
            "games": total
        }
    except:
        return {"error": "Team not found"}

def get_player_stats(player_name: str, stat_type: str = "season") -> Dict:
    """Get player statistics"""
    try:
        players = pd.read_csv(os.path.join(DATA_PATH, "data", "afl_datasets", "afl_players_info_raw.csv"))
        player = players[players['player_name'].str.contains(player_name, case=False, na=False)]
        
        if player.empty:
            return {"error": "Player not found"}
        
        player_id = player.iloc[0]['id']
        
        stats = pd.read_csv(os.path.join(DATA_PATH, "player_game_eda.csv"))
        player_stats = stats[stats['player_id'] == player_id]
        
        if player_stats.empty:
            return {"error": "No stats found"}
        
        return {
            "player": player.iloc[0]['player_name'],
            "games": len(player_stats),
            "avg_disposals": round(player_stats['disposals_target'].mean(), 1),
            "avg_goals": round(player_stats['goals_target'].mean(), 1),
            "avg_fantasy": round(player_stats['fantasy_target'].mean(), 1)
        }
    except:
        return {"error": "Error retrieving stats"}

def get_head_to_head(team_a: str, team_b: str) -> Dict:
    """Get historical matchup record"""
    try:
        matches = pd.read_csv(os.path.join(DATA_PATH, "home_matches_eda.csv"))
        h2h = matches[
            ((matches['team_name'] == team_a) & (matches['opponent'] == team_b)) |
            ((matches['team_name'] == team_b) & (matches['opponent'] == team_a))
        ]
        
        team_a_wins = len(h2h[(h2h['team_name'] == team_a) & (h2h['home_win'] == 1)])
        team_b_wins = len(h2h[(h2h['team_name'] == team_b) & (h2h['home_win'] == 1)])
        
        return {
            "team_a": team_a,
            "team_b": team_b,
            "team_a_wins": team_a_wins,
            "team_b_wins": team_b_wins,
            "total_meetings": len(h2h)
        }
    except:
        return {"error": "Error retrieving head-to-head"}

# ============================================================================
# GUARDRAILS
# ============================================================================

OFF_TOPIC_KEYWORDS = ['weather', 'mausam', 'politics', 'siasat', 'cricket', 'khana', 'movie', 'film', 'song']

def is_off_topic(query: str) -> bool:
    """Check if query is off-topic"""
    query_lower = query.lower()
    return any(kw in query_lower for kw in OFF_TOPIC_KEYWORDS)

def get_refusal_response() -> str:
    """Get polite refusal response"""
    return "Main sirf AFL ki madad kar sakta hoon. Kya aap koi AFL team, player, ya match ke baare mein jaanna chahte hain?"

# ============================================================================
# MEMORY
# ============================================================================

class ConversationMemory:
    def __init__(self):
        self.history = []
    
    def add(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        if len(self.history) > 10:
            self.history.pop(0)
    
    def get_context(self) -> str:
        return "\n".join([f"{m['role']}: {m['content']}" for m in self.history[-5:]])
    
    def resolve_reference(self, query: str) -> str:
        """Resolve references like 'us se sasti'"""
        if "sasti" in query.lower() or "cheaper" in query.lower():
            # Find last mentioned property
            for msg in reversed(self.history):
                if msg["role"] == "assistant" and "PKR" in msg["content"]:
                    return f"cheaper than previously mentioned"
        return query

# ============================================================================
# AGENT
# ============================================================================

class AFLChatAgent:
    def __init__(self):
        self.memory = ConversationMemory()
    
    def chat(self, message: str) -> str:
        """Process message and return response"""
        self.memory.add("user", message)
        
        # Check off-topic
        if is_off_topic(message):
            response = get_refusal_response()
            self.memory.add("assistant", response)
            return response
        
        # Route to appropriate tool
        message_lower = message.lower()
        
        if any(kw in message_lower for kw in ['record', 'win', 'loss', 'season']):
            # Team record query
            response = self._handle_team_query(message)
        elif any(kw in message_lower for kw in ['player', 'stats', 'disposals', 'goals']):
            # Player stats query
            response = self._handle_player_query(message)
        elif any(kw in message_lower for kw in ['head to head', 'h2h', 'matchup']):
            # Head-to-head query
            response = self._handle_h2h_query(message)
        else:
            # General AFL knowledge
            response = self._handle_general_query(message)
        
        self.memory.add("assistant", response)
        return response
    
    def _handle_team_query(self, message: str) -> str:
        # Extract team name (simplified)
        teams = ['Collingwood Magpies', 'Carlton Blues', 'Hawthorn Hawks', 'Richmond Tigers']
        for team in teams:
            if team.lower() in message.lower():
                record = get_team_record(team)
                if "error" not in record:
                    return f"{team}: {record['wins']} wins, {record['losses']} losses ({record['win_rate']:.0%} win rate)"
        return "Team nahi mili. Kya aap kisi specific team ke baare mein jaanna chahte hain?"
    
    def _handle_player_query(self, message: str) -> str:
        return "Player stats ke liye player ka naam batayein."
    
    def _handle_h2h_query(self, message: str) -> str:
        return "Head-to-head record ke liye dono teams ke naam batayein."
    
    def _handle_general_query(self, message: str) -> str:
        return "Main AFL expert hoon. Aap kisi bhi team, player, ya match ke baare mein pooch sakte hain."

if __name__ == "__main__":
    agent = AFLChatAgent()
    print(agent.chat("Assalam-o-Alaikum"))
    print(agent.chat("Collingwood ka record kya hai?"))
    print(agent.chat("What's the weather?"))