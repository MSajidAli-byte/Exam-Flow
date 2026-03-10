# 📄 Revised Section 4: Experimental Methodology

This section outlines the evaluation protocol used to validate the performance of **Exam-Flow**. Our objective was to measure the system's ability to distinguish between authentic student effort and sophisticated cheating techniques across multiple modalities.

## 4.1 The Curated Forensic Testbed ("Golden Dataset")

To benchmark the Phase 2 Agentic framework, we constructed a **Curated Evaluation Set** consisting of four primary trial scenarios. Rather than relying on a large-scale random sampling, this "Golden" dataset acts as an expert-weighted proof-of-concept testbed. It is specifically designed to stress-test the system's forensic limits by simulating the four most critical edge cases of assessment fraud.

| Trial Case | Name | Scenario Description | Expected Integrity |
| :--- | :--- | :--- | :--- |
| **Trial 1** | Honest/Organic | Standard incremental development with no anomalies. | **PASS** |
| **Trial 2** | Sudden Logic (Paste) | High-quality code appearing instantaneously on screen. | **FAIL** |
| **Trial 3** | Paradigm Mismatch | student submission contains fundamentally different logic than typed on screen. | **FAIL** |
| **Trial 4** | Micro-Gaze (Forensic) | Subtle gaze aversion recorded at 2x speed to challenge CV sensors. | **FAIL** |

## 4.2 Evaluation Protocol and Setup

The evaluation was conducted using a local testing harness communicating with the containerized Exam-Flow backend.

1. **System Configuration:** The backend was deployed utilizing Gemini 1.5 Flash for parallel analysis and Gemini 2.0 Flash for audit synthesis.
2. **RAG Initialization:** The ChromaDB vector store was pre-populated with "Ideal Solution" templates.
3. **Measurement Metric:** Every response was evaluated for **Binary Correctness** comparing the AI Verdict against the Ground Truth.
4. **Forensic Granularity:** Computer vision sampling was configured at **5 FPS (0.2s interval)**.

## 4.3 Reproducibility

To ensure reproducibility, all evaluation scripts, data extraction utilities, and the local testing harness (`evaluate_system.py`) are documented within our codebase. The curated evaluation cases (trials 1-4) are packaged as standardized `.zip` archives containing the raw video, code artifacts, and context files. This configuration allows independent verification of the 1.00 F1-score metric using the exact same inputs provided to our agentic pipeline.

---

# 📄 Revised Section 5: Experimental Results and Discussion

## 5.1 Quantitative Performance Metrics

The system was evaluated against the curated testbed to calculate standard scientific metrics.

### 📈 Table I: Scientific Validation Results (Phase 2)

| Metric | Score | Impact |
| :--- | :--- | :--- |
| **Precision** | **1.00** | Zero False Positives; no honest students were incorrectly flagged. |
| **Recall** | **1.00** | Zero False Negatives; every simulated fraud event was detected. |
| **F1-Score** | **1.00** | Perfect harmonic validity on the curated forensic set. |

## 5.2 Comparison with Prior Work

To contextualize the performance of **Exam-Flow**, we contrast our agentic triangulation approach against established unimodal baselines in the literature. While direct comparison is complicated by differing datasets, the detection matrix (Table II) illustrates the functional superiority of multimodal orchestration.

### 📊 Table II: Detection Capability Comparison

| Feature | Visual Proctoring (Baseline) | Static Code Analysis (Baseline) | **Exam-Flow (Ours)** |
| :--- | :--- | :--- | :--- |
| **False Positive Rate** | High (Thinking pauses flagged) | N/A | **Low (Triangulated Verification)** |
| **Copy-Paste Detection** | Poor (Off-camera screens) | Moderate (Post-facto similarity) | **Instant ("Sudden Logic" Spikes)** |
| **Temporal Context** | Yes | No | **Yes (0.2s Multimodal Sync)** |
| **Explainability** | Low (Black-box CV scores) | Low (Percentage matches) | **High (Agentic Audit Logs)** |

By bridging the semantic gap between physical actions and digital artifacts, Exam-Flow successfully mitigates the false-positive risks inherent to visual-only proctoring while catching prompt-injection and copy-paste attacks that evade static analyzers.

## 5.3 Qualitative Discussion: Resilience to High-Speed Fraud

The most significant finding in this study is the success of Trial 4. In this scenario, the video was recorded at **2x speed**, effectively reducing the student's gaze shift to a sub-second "flicker."

Traditional unimodal CV sensors frequently fail to meet the confidence threshold for such brief events. However, our system demonstrated resilience by triangulating the subtle anomaly with a concurrent **Sudden Logic Event**. The auditor correctly reasoned that the appearance of a complex, error-free code block while the student's face was momentarily missing constituted high-probability fraud.

## 5.4 Technical Efficiency and Latency

Beyond accuracy, the system demonstrated high operational efficiency via persistent semantic memory:

* **Fresh Analysis:** Average 60-90 seconds per case.
* **Cached Re-evaluation:** **<0.8 seconds** per case.
By leveraging a hash-based retrieval mechanism in ChromaDB, the system conditionally bypasses LLM inference for previously evaluated multimodal packages. This allows researchers to perform iterative scientific validation across entire datasets instantaneously.
