# 🎥 Exam-Flow Phase 2: Client Demo & Handover Script

**Goal:** Demonstrate the transition from Phase 1 (Linear AI) to Phase 2 (Agentic Multi-Modal Architecture), highlighting the robust backend, RAG integration, and scientific validation.

---

## 🎬 Scene 1: Introduction & Documentation

**Action:**

1. Open VS Code.
2. Close all tabs except `PHASE2_CLIENT_HANDOVER.md`.
3. Close the terminal panel for a clean view.

**Voiceover:**
"Welcome to the Phase 2 delivery of Exam-Flow. In this demo, we'll transition the system from the linear Phase 1 prototype to the fully autonomous, multi-agent architecture we've built. We'll follow the exact steps documented in `PHASE2_CLIENT_HANDOVER.md`, which serves as your primary guide for deployment."

---

## 🎬 Scene 2: Configuration & The "Switch"

**Action:**

1. Open `.env` file (or show a dummy one if sensitive).
2. Highlight the `PHASE` and `AGENTIC_MODE` variables.

**Voiceover:**
"The shift to Phase 2 is controlled by simple environment flags. We set `PHASE=2` and `AGENTIC_MODE=on`. This tells the backend to bypass the simple linear grader and instead engage the Agent Orchestrator, which manages our team of four specialized AI agents."

---

## 🎬 Scene 3: The New Architecture (Code Walkthrough)

**Action:**

1. Open the file explorer to `services/backend/agents/`.
2. Click and show `orchestrator.py`.
3. Briefly click `visual_proctor.py`, `code_reviewer.py`, `integrity_auditor.py`.
4. Open `services/backend/rag/rag_manager.py`.

**Voiceover:**
"Before we run it, let's look at the new engine.

- Here in the `agents` folder, you see the specialized workforce: The **Visual Proctor** for behavioral analysis, the **Code Reviewer** for technical grading, and the **Integrity Auditor** which cross-references them.
- They are coordinated by this **Orchestrator** (`orchestrator.py`).
- And crucially, we've added **RAG (Retrieval Augmented Generation)** here in `rag_manager.py`. This connects the AI to a 'Gold Standard' library of ideal solutions, ensuring grading is based on facts, not hallucinations."

---

## 🎬 Scene 4: Deployment & Initialization

**Action:**

1. Open the Integrated Terminal.
2. Run: `docker-compose down`
3. Run: `docker-compose up --build -d`
4. Wait for the logs: `Attaching to exam-flow-backend-1...`

**Voiceover:**
"We'll now spin up the new architecture using Docker Compose. This rebuilds the containers to include the new dependencies like ChromaDB for our vector memory."

**Action:**
5.  Once running, execute the RAG initialization command:
    `docker exec exam-flow-backend-1 python init_rag.py`

**Voiceover:**
"This is a critical Phase 2 step. We are initializing the Expert Knowledge Base. You can see it's adding 'Gold Standard' solutions for Java, Docker, and Python into our vector database. The agents will reference these during grading."

---

## 🎬 Scene 5: The "Solution Package" Demo (ZIP Upload)

**Action:**

1. Open browser to `http://localhost:8501`.
2. Select **"Solution Package (ZIP)"**.
3. Upload `case1_standard_success.zip`.
4. Click **"Analyze Solution Package"**.
5. Switch back to VS Code Terminal **briefly** to show the logs scrolling (`Agent A starting... Agent B starting...`).
6. Switch back to UI to show the final report.

**Voiceover:**
"Let's test the full pipeline. Phase 2 supports a 'Solution Package' upload—containing video, code, and context files.
As the analysis runs, you can see on the backend that the agents are firing sequentially: Visual Proctor first, then Code Reviewer, then the Integrity Audit.
...
And here is the result. Notice the detailed breakdown: A separate technical score, a management score, and a specific Integrity Status. The system has certified this submission."

---

## 🎬 Scene 6: Single Video Fallback (Restored Feature)

**Action:**

1. Refresh page or clear upload.
2. Select **"Single Video"**.
3. Upload `Java_Demo_Exam-Flow.mp4`.
4. Show the result (likely Flagged for Sudden Logic/Pasting).

**Voiceover:**
"We've also maintained backward compatibility for Single Video uploads. In this mode, the Code Reviewer automatically switches to 'Visual Analysis'—literally reading the code from the screen.
However, notice the strictness of Phase 2: because this demo video shows code appearing instantly, the Integrity Auditor flags it as 'Sudden Logic' or pasting, and caps the score. This demonstrates the new security protocols in action."

---

## 🎬 Scene 7: Scientific Validation (Optional/Power User)

**Action:**

1. Go back to VS Code.
2. Open `research/evaluate_system.py`.
3. Show the `GROUND_TRUTH` dictionary.
4. Run: `python research/evaluate_system.py` (Let it run for 10s then stop, or show pre-run results).

**Voiceover:**
"Finally, Phase 2 isn't just code; it's research. We've included this `evaluate_system.py` script. It runs the AI against a battery of 7 known test cases—cheaters, innocent students, and edge cases—to scientifically calculate the system's Precision and Recall. This confirms the system is statistically accurate, not just guessing."

---

## 🎬 Scene 8: Conclusion

**Action:**

1. Show the `PHASE2_CLIENT_HANDOVER.md` again.

**Voiceover:**
"The entire Phase 2 system—Files, Docker config, and RAG database—is fully packaged and ready for handover. You can follow the guide to deploy this immediately."
