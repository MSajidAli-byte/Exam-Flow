# 🛠️ Methodology: The Exam-Flow Agentic Architecture

The core of the **Exam-Flow** framework is its **Multi-Agent Orchestration Engine**, which transitions from traditional monolithic LLM grading to a sequentially coordinated pipeline of 4 specialized agents. This architecture enables the system to perform **Forensic Triangulation** by correlating behavioral data, screen activity, and source code evolution.

## 1. The Orchestration Pipeline (`orchestrator.py`)

The system follows a 4-step sequential workflow, integrated with a **ChromaDB RAG (Retrieval-Augmented Generation)** layer:

1. **Context Loading (RAG Manager):**
    Before any analysis, the system retrieves the most relevant "Ideal Solution" from a persistent knowledge base. This ensures the AI has a ground-truth baseline for coding patterns and architectural norms.
2. **Multimodal Asset Preparation:**
    The screen recording is uploaded via the Gemini Files API. One single file handle is shared across all subsequent agents, significantly reducing API latency and preventing redundant video processing.

## 2. Agent Roles and Forensic Responsibilities

### **Agent A: The Visual Proctor (Behavioral Monitor)**

* **Input:** OpenCV Gaze/Face logs + Gemini Video Stream.
* **Responsibility:** Performs sub-second (0.2s) forensic sampling of the student's behavior. It specifically looks for micro-gaze aversions (detectable even in 2x speed videos) and correlates them with facial visibility logs.
* **Result:** A behavioral anomaly report with timestamps and high-fidelity descriptions of visual breaches.

### **Agent B: The Code Reviewer (Process Monitor)**

* **Input:** Submitted Source Code + Gemini Video Stream (Screen).
* **Responsibility:** Monitors the **Code Production Process**. It compares the final submitted code against the incremental typing seen on the screen recording.
* **Key Detection:** Identifies **"Sudden Logic Events"** (e.g., complex blocks appearing in <1s) which indicate copy-pasting from external sources.

### **Agent C: The Integrity Auditor (The "Skeptical" Triangulator)**

* **Input:** Agent A Report + Agent B Report + Video Stream.
* **Responsibility:** Cross-references behavioral flags with code entry speed. It is designed to be highly skeptical, looking for "Incongruent Patterns"—for example, complex algorithms being error-free on first entry while the student is momentarily looking away.
* **Verdict:** This agent issues the definitive `INVESTIGATION` or `PASS` status.

### **Agent D: The Final Grader (The Synthesizer)**

* **Input:** All previous Agent reports + Original Rubric.
* **Responsibility:** Combines technical scoring (pre-audit) with the integrity verdict.
* **The Integrity Cap Policy:** If Agent C issues a `FAIL` or `INVESTIGATION`, the Final Grader applies a mandatory **20/100 grade cap**, ensuring that even "perfect" code cannot bypass integrity failures.

## 3. The "Smart Caching" System

To support large-scale research, the architecture includes a **Persistent Caching Layer**. Analysis results are tagged with a `source: Cached Research Result` flag. If a case (like Trial 1) is re-evaluated, the system skips the 60-90s AI processing time and provides the result in **<1s**, allowing for instantaneous scientific validation.
