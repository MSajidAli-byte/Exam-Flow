# 📄 Section 3: Methodology (The Agentic Orchestration Model)

This section describes the technical architecture and the multi-agent orchestration strategy of **Exam-Flow**. The system transitions from a traditional monolithic analysis to a **High-Fidelity Forensic Pipeline**, which relies on a sequentially coordinated team of specialized Large Language Model (LLM) agents.

## 3.1 The Multi-Agent Orchestration Framework

The core innovation of Exam-Flow is the shift from observation to **Triangulation**. Rather than relying on a single vision sensor or a code similarity check, the framework uses an **Agentic Orchestrator** to synchronize disparate data streams (Video, Screen, Code, and RAG-based context).

### 3.1.1 The Analysis Pipeline

The orchestration follows a four-stage sequential workflow:

1. **Context Injection (RAG Layer):** The system first retrieves "Ideal Solution" patterns from a persistent **ChromaDB** knowledge base, providing agents with a grounding context for the specific exam topic.
2. **Asset Normalization:** Screen recordings are uploaded to the Gemini Files API and distributed to agents via a shared file handle, ensuring temporal consistency across all analysis reports.

## 3.2 Agent Roles and Specializations

Each agent in the pipeline is designed with a specific forensic persona and a unique set of sensory inputs.

### **Agent A: The Visual Proctor (Behavioral Forensic Expert)**

* **Sensor Input:** OpenCV Haar-Cascade Eye/Face Detection + Raw Webcam Video.
* **Methodology:** Performs ultra-forensic sampling at **0.2s (5 FPS)** intervals. It is specifically designed to confirm if low-level CV flags (Gaze Aversion) correlate with actual physical behavior in the recording, especially in **high-speed (2x)** video modes.

### **Agent B: The Code Reviewer (Process Integrity Expert)**

* **Sensor Input:** Submitted Source Code + Screen Recording.
* **Methodology:** Simultaneously reads the final code file while "watching" the screen. It maps the timeline of code entry to identify **Sudden Logic Events**—complex algorithmic blocks that appear instantaneously ( < 3 seconds), indicating external code transfer rather than organic typing.

### **Agent C: The Integrity Auditor (The "Skeptical" Triangulator)**

* **Sensor Input:** Reports from Agent A & Agent B + Raw Screen Video.
* **Methodology:** Acts as the critical decision engine. It cross-references discrepancies, such as complex code appearing (Agent B flag) while the student is momentarily looking away or the face is absent (Agent A flag). This triangulation enables the system to detect fraud even if individual sensors are temporarily masked or challenged by recording conditions.

### **Agent D: The Final Grader (The Forensic Synthesizer)**

* **Methodology:** Consolidates technical proficiency scores with integrity audits.
* **The Integrity Penalty Rule:** The system enforces a mandatory **Integrity Cap of 20/100** for any submission flagged with a `FAIL` or `INVESTIGATION` status by the Auditor, regardless of the functional quality of the code.

## 3.3 Adaptive Caching and Speed-to-Science

To support large-scale educational research, the system utilizes an **Experimental Caching Layer**. Analysis artifacts are indexed by unique case IDs. Retrospective evaluations of previously analyzed trials (e.g., Trial 1-4) result in instantaneous responses (**<1s latency**), allowing researchers to perform rapid iterative scientific validation without repeated API cooldown delays.
