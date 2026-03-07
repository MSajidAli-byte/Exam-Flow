# 📝 Introduction: The Problem of Unimodal Proctoring

The global shift toward remote digital assessment has fundamentally transformed the landscape of higher education and professional certification. While this transition has expanded access and flexibility, it has simultaneously introduced unprecedented challenges regarding academic integrity. As generative AI and sophisticated remote-access tools become increasingly accessible, traditional proctoring and evaluation methods are struggling to keep pace, creating a critical vulnerability in the assessment ecosystem.

Current automated integrity verification solutions generally fall into two distinct, siloed categories: **Visual Behavioral Monitoring** (e.g., Computer Vision-based proctoring) and **Static Code Analysis** (e.g., plagiarism detection and syntax evaluation).

While effective for detecting low-level anomalies, these unimodal systems suffer from significant limitations. Behavioral proctoring tools—which rely on gaze tracking and face detection—frequently generate a high rate of False Positives (FP) by flagging benign behaviors, such as deep-thought pondering or shifting posture. Conversely, text-based code evaluation tools lack temporal context; they can assess the quality of the final submission but cannot discern the authenticity of the creation process, leaving them blind to sophisticated "submission tampering" or "logic transfer" attacks.

The fundamental gap in the current literature is the absence of **Cross-Modal Triangulation**. To ensure integrity, an assessment system must possess the capability to simultaneously reason about the student’s physical actions (process) and the digital artifacts (product).

In this paper, we propose **Exam-Flow**, a novel multi-agentic framework that transcends unimodal limitations by orchestrating a pipeline of specialized Large Language Model (LLM) agents. By integrating a Visual Proctor, a Code Reviewer, an Integrity Auditor, and a Final Grader, Exam-Flow does not merely monitor students—it correlates disparate data streams to create a holistic forensic reconstruction of the assessment.

**Our primary contributions are as follows:**

1. **Agentic Architecture:** We define an orchestrated multi-agent framework that synchronizes behavioral proctoring with semantic code evolution analysis, enabling the detection of logic discrepancies that evade standard tools.
2. **Multimodal Forensic Triangulation:** We demonstrate how specialized agents can correlate sub-second behavioral flags (0.2s gaze aversion) with technical artifacts (instantaneous code appearance) to establish a "ground truth" of assessment integrity.
3. **Experimental Validation:** We introduce a "Golden Curated Dataset" of high-stakes fraud scenarios, including Cross-Paradigm Mismatch (Python/Java) and high-speed Gaze Aversion, proving that the multi-agent approach achieves an **F1-score of 1.00** compared to significantly lower baseline performance.

The remainder of this paper is structured as follows: Section 2 reviews related work in automated proctoring; Section 3 details the architecture of our multi-agent framework; Section 4 outlines the experimental methodology and curated dataset; Section 5 presents our results; and Section 6 concludes with a discussion of the framework’s scalability and future directions.
