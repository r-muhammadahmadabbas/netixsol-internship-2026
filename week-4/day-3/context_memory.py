"""
Day 3: Context Memory
Multi-turn conversation memory with reference resolution
"""

class ConversationMemory:
    def __init__(self):
        self.short_term = []
        self.long_term = {}
    
    def add_turn(self, user_msg, agent_msg, extracted_info):
        self.short_term.append({
            "user": user_msg,
            "agent": agent_msg,
            "info": extracted_info
        })
        if len(self.short_term) > 10:
            self.short_term.pop(0)
    
    def get_context(self):
        return {
            "recent": self.short_term[-5:],
            "preferences": self.long_term.get("preferences", {}),
        }
    
    def resolve_reference(self, query):
        """Resolve 'us se sasti' -> cheaper than last mentioned property"""
        last_property = self._get_last_mentioned_property()
        if "sasti" in query and last_property:
            return f"cheaper than {last_property}"
        return query
    
    def _get_last_mentioned_property(self):
        for turn in reversed(self.short_term):
            if "property" in turn.get("info", {}):
                return turn["info"]["property"]
        return None

if __name__ == "__main__":
    memory = ConversationMemory()
    memory.add_turn("Budget 3 crore hai", "Samajh gaya", {"budget": 30000000})
    memory.add_turn("DHA mein kya options?", "Yeh rahi options", {"area": "DHA", "property": "DHA Phase 5"})
    memory.add_turn("Us se sasti koi option?", "Ji sir", {})
    
    print("Memory test:")
    print(f"  Budget: {memory.get_context()['preferences']}")
    print(f"  Resolved: {memory.resolve_reference('Us se sasti koi option?')}")