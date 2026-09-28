from src.agent import run_agent

r1 = run_agent("Payment plan for DHA Phase 5 kya hai?")
print("RAG:", r1["intent"], "|", r1["response"][:60])

h = [{"role": "user", "content": "Budget 3 crore, Lahore DHA"}, {"role": "assistant", "content": "Options"}]
r2 = run_agent("Visit book karni hai 20/01/2025 10:00", history=h)
print("Booking:", r2["intent"], "| Event:", r2.get("event_id") is not None)

r3 = run_agent("Ye bohat mehenga hai")
print("Objection:", r3["intent"], "|", r3["response"][:60])

r4 = run_agent("What is the weather?")
print("Off-topic:", r4["intent"])
