# 📄 Detailed Research Abstract: Exam-Flow Framework

**Title:** Exam-Flow: An Agentic Multimodal Framework for Automated Academic Integrity Verification

**Abstract:**
With the rapid proliferation of remote technical assessments, maintaining academic integrity has become a critical challenge for educational institutions and professional certification bodies. Traditional automated proctoring systems often rely on unimodal computer vision (CV) or rigid plagiarism detection algorithms, which are susceptible to sophisticated cheating techniques and high false-positive rates. This paper introduces **Exam-Flow**, a novel multi-agentic framework designed to synchronize behavioral proctoring with semantic code analysis through an orchestrated pipeline of Large Language Model (LLM) agents.

Our framework employs four specialized agents: a **Visual Proctor** for sub-second (0.2s) gaze and facial tracking, a **Code Reviewer** for real-time screen-to-code synchronization, an **Integrity Auditor** for cross-modal triangulation, and a **Final Grader** for synthesized verdict production. We evaluate Exam-Flow using a curated "Golden Dataset" containing diverse fraud scenarios, including instantaneous code-pasting, architectural tampering, and micro-gaze aversions in high-speed (2x) recordings.

Experimental results demonstrate that Exam-Flow achieves an **F1-score of 1.00**, accurately distinguishing between organic incremental development and fraudulent behavior where baseline unimodal systems failed. Furthermore, the integration of a **Smart Caching Engine** reduces subsequent evaluation latency from over 60 seconds to less than 1 second per case. This study proves that agentic triangulation provides a robust, scalable, and highly precise solution for autonomous high-stakes assessment proctoring in the era of generative AI.

---
**Keywords:** Multi-modal AI, Agentic Frameworks, Academic Integrity, Automated Proctoring, LLM Orchestration.
