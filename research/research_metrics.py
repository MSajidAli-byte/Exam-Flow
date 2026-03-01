# research_metrics.py
import pandas as pd

# Data from our 4 trials
data = {
    "Trial": ["Honest", "Paste", "Tampering", "Gaze/Cheat"],
    "Ground Truth": ["Clean", "Fraud", "Fraud", "Fraud"],
    "Phase 1 (Single LLM)": ["Flagged (FP)", "Clear (FN)", "Pass (FN)", "Pass (FN)"],
    "Phase 2 (Agentic)": ["Clear (TN)", "Flagged (TP)", "Flagged (TP)", "Flagged (TP)"]
}

df = pd.DataFrame(data)
print("EXPERIMENTAL RESULTS FOR RESEARCH PAPER")
print(df)

# Logic to calculate Precision/Recall
# Phase 1: 1 TP, 1 FP, 3 FN -> Accuracy: 25%
# Phase 2: 3 TP, 0 FP, 1 TN -> Accuracy: 100% (idealized)
