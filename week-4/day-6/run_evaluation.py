"""
Day 6: Evaluation Suite
40+ test cases across 11 categories
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from evaluation import run_evaluation

if __name__ == "__main__":
    run_evaluation()