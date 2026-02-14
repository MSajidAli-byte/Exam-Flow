# 🔬 Phase 2: Scientific Research Protocol

## "The Expert-Led Validation System"

This document outlines the conditions and procedures for running the scientific evaluation of the Exam-Flow Agentic AI system. This protocol is designed to generate the **Precision, Recall, and F1-Score** metrics required for academic validation.

---

### 📋 1. Prerequisites (Usage Conditions)

Before running the evaluation, the following conditions MUST be met:

1. **API Key Eligibility**: You must have a valid `GOOGLE_API_KEY` in your `.env` file.
2. **Phase 2 Activation**: The environment variable `AGENTIC_MODE=on` must be set.
3. **Library Seeding (RAG)**: The Expert Solution Library must be populated.
    * *Command*: `docker exec exam-flow-backend-1 python init_rag.py`
4. **ChromaDB Status**: The backend must be healthy and the database must be persistent.

---

### 🛠️ 2. Validation Procedure

#### **Step 1: Generate the Golden Dataset**

This script creates 7 diverse "Solution Packages" (ZIPs) that include video, code, and context. These represent different behaviors (Standard, Logic Injection, Gaze Aversion, etc.).

* **Action**: Run `python research/generate_dataset.py` from the project root.
* **Result**: 7 ZIP files appear in `research/cases/`.

#### **Step 2: Execute Scientific Evaluation**

This script iterates through all 7 cases, sends them to the Agentic Team, and compares the AI's verdict against the "Ground Truth."

* **Action**: Run `python research/evaluate_system.py` from the project root.
* **Note**: This script uses a **30-second logic delay** between cases to respect the Free Tier API limits.

---

### 📊 3. Interpreting the Metrics

At the end of the script, you will see a summary table:

| Metric | Definition | Importance for Research |
| :--- | :--- | :--- |
| **Precision** | How many "Cheater" flags were actually cheaters? | Measures the "False Positive" rate. |
| **Recall** | How many total cheaters did we successfully catch? | Measures the "Safety" of the system. |
| **F1-Score** | The harmonic mean of Precision and Recall. | The definitive score of system accuracy. |

---

### ⚠️ 4. Troubleshooting & Quota Limits

* **429 Error**: If you see a quota error, simply wait 60 seconds and restart the script. The `Tenacity` retry logic I implemented will handle most small interruptions.
* **404 Error**: Ensure the ZIP files exist in `research/cases/` before running the evaluation.
