# Week 2 Day 4 — CrewAI — Multi-Agent Collaboration

## Status
- [x] Task 1: Multi-Agent Design Thinking
- [x] Task 2: Build Agents & Assign Tools
- [x] Task 3: Define Tasks & Process
- [x] Task 4: Try Hierarchical Delegation
- [x] Task 5: Evaluation & Cost Awareness

## Deliverables
- `task3_runner.py` — Sequential crew (Task 3)
- `task4_runner.py` — Hierarchical crew (Task 4)
- `task5_runner.py` — Evaluation & cost comparison (Task 5)
- `writeup.md` — Short write-up (convert to PDF)
- `notes.md` — Detailed notes for all 5 tasks

## How to Run
```bash
# Run Task 3 (Sequential)
python task3_runner.py

# Run Task 4 (Hierarchical)
python task4_runner.py

# Run Task 5 (Evaluation)
python task5_runner.py
```

Or from Jupyter:
```python
!python C:\Internship\Netixsol\week-2\day-4\task3_runner.py
!python C:\Internship\Netixsol\week-2\day-4\task4_runner.py
!python C:\Internship\Netixsol\week-2\day-4\task5_runner.py
```

## Business Task
"Research a competitor (Canva), summarize findings, and draft a marketing angle"

## Agents
| Agent | Role | Temperature |
|-------|------|-------------|
| Researcher | Gather factual data | 0.0 |
| Analyst | Synthesize into insights | 0.3 |
| Strategist | Draft marketing angle | 0.7 |

## Results
| Approach | Tokens | Cost | Quality |
|----------|--------|------|---------|
| Sequential | ~5000 | ~$0.0014 | 4.67/5 |
| Hierarchical | ~7000 | ~$0.0019 | 5.00/5 |
