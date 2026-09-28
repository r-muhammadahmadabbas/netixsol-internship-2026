"""
Day 3: Natural Speech Behaviors
Fillers, hesitations, acknowledgements for human-like conversation
"""

NATURAL_BEHAVIORS = {
    "thinking": ["Hmm...", "Acha...", "Ji... ek second...", "Let me check..."],
    "acknowledge": ["Ji haan", "Samajh gaya", "Theek hai", "Bilkul"],
    "hesitation": ["Umm...", "Ji...", "Ek minute..."],
    "laughter": ["Haha", "Hehe", "Ji sir!"],
    "correction": ["Sorry, wo nahi...", "Mera matlab tha..."],
    "code_switching": ["Ji sir, budget 3 crore hai, let me check DHA options", "Payment plan flexible hai, monthly sirf 60k"]
}

def inject_natural_behavior(text, context):
    """Inject natural behaviors based on context"""
    import random
    if context == "tool_calling":
        prefix = random.choice(NATURAL_BEHAVIORS["thinking"])
    elif context == "listening":
        prefix = random.choice(NATURAL_BEHAVIORS["acknowledge"])
    return f"{prefix} {text}"

if __name__ == "__main__":
    print("Natural Speech Behaviors:")
    for behavior, examples in NATURAL_BEHAVIORS.items():
        print(f"\n{behavior.upper()}:")
        for ex in examples:
            print(f"  - {ex}")