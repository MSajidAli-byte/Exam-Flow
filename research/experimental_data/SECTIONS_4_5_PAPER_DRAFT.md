# 📄 Section 4: Experimental Methodology

This section outlines the evaluation protocol used to validate the performance of **Exam-Flow**. Our objective was to measure the system's ability to distinguish between authentic student effort and sophisticated cheating techniques across multiple modalities.

## 4.1 The "Golden" Curated Dataset

To benchmark the Phase 2 Agentic framework, we constructed a **Curated "Golden" Dataset** consisting of four primary trial scenarios. Unlike large-scale synthetic datasets, these cases were specifically designed to test the system’s forensic limits, particularly focusing on temporal and semantic discrepancies.

| Trial Case | Name | Scenario Description | Expected Integrity |
| :--- | :--- | :--- | :--- |
| **Trial 1** | Honest/Organic | Standard incremental development with no anomalies. | **PASS** |
| **Trial 2** | Sudden Logic (Paste) | High-quality code appearing instantaneously on screen. | **FAIL** |
| **Trial 3** | Paradigm Mismatch | student submission contains fundamentally different logic than typed on screen (e.g., Python vs. Java). | **FAIL** |
| **Trial 4** | Micro-Gaze (Forensic) | Subtle gaze aversion recorded at 2x speed to challenge CV sensors. | **FAIL** |

## 4.2 Evaluation Protocol and Setup

The evaluation was conducted using a local testing harness (`evaluate_system.py`) communicating with the containerized Exam-Flow backend.

1. **System Configuration:** The backend was deployed in **Expert Agentic (Phase 2)** mode, utilizing Gemini 1.5 Flash for parallel analysis and Gemini 2.0 Flash for audit synthesis.
2. **RAG Initialization:** The ChromaDB vector store was pre-populated with "Ideal Solution" templates for Data Structures and Algorithms to ground the code review agents.
3. **Measurement Metric:** Every response was evaluated for **Binary Correctness** comparing the AI Verdict against the Ground Truth.
4. **Forensic Granularity:** Computer vision sampling was configured at **5 FPS (0.2s interval)** to ensure the detection of micro-anomalies in high-speed recordings.

---

# 📄 Section 5: Experimental Results and Discussion

This section presents the quantitative performance metrics and a deep qualitative analysis of the forensic triangulation process.

## 5.1 Quantitative Performance Metrics

The system was evaluated against the "Golden Dataset" to calculate standard scientific metrics: **Precision**, **Recall**, and **F1-Score**.

### 📈 Table II: Scientific Validation Results (Phase 2)

| Metric | Score | Impact |
| :--- | :--- | :--- |
| **Precision** | **1.00** | Zero False Positives; no honest students were incorrectly flagged. |
| **Recall** | **1.00** | Zero False Negatives; every simulated fraud event was detected. |
| **F1-Score** | **1.00** | Perfect harmonic validity on the curated forensic set. |

### 📑 Table III: Case-by-Case Breakdown

| Trial Name | Ground Truth | AI Prediction | Result | Detection Vector |
| :--- | :--- | :--- | :--- | :--- |
| `trial1_honest.zip` | PASS | **PASS** | ✅ MATCH | Multi-Agent Consensus |
| `trial2_sudden_logic.zip` | FAIL | **FAIL** | ✅ MATCH | Code Reviewer (Logic Spike) |
| `trial3_paradigm_mismatch.zip` | FAIL | **FAIL** | ✅ MATCH | Auditor (Cross-Modal Diff) |
| `trial4_gaze_aversion.zip` | FAIL | **FAIL** | ✅ MATCH | Forensic Triangulation |

## 5.2 Qualitative Discussion: Resilience to High-Speed Fraud (Trial 4)

The most significant finding in this study is the success of Trial 4. In this scenario, the video was recorded at **2x speed**, effectively reducing the student's gaze shift to a sub-second "flicker."

Traditional unimodal CV sensors frequently fail to meet the confidence threshold for such brief events. However, the **Exam-Flow Integrity Auditor** demonstrated resilience by triangulating the subtle visual anomaly with a concurrent **Sudden Logic Event** (detected by Agent B). The auditor correctly reasoned that the appearance of a complex, error-free code block while the student's face was momentarily missing or eyes were averted constituted high-probability fraud.

## 5.3 Technical Efficiency and Latency

Beyond accuracy, the system demonstrated high operational efficiency:

* **Fresh Analysis:** Average 60-90 seconds per case.
* **Cached Re-evaluation:** **<0.8 seconds** per case.
The **Smart Caching Layer** significantly outperformed the Phase 1 baseline, which required a manual cooldown periods for every repeated run. This efficiency allows researchers to perform iterative scientific validation across entire datasets in seconds.
