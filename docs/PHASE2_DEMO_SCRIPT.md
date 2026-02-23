# 🎥 Exam-Flow Phase 2: Client Demo & Handover Script

**Goal:** Demonstrate the seamless upgrade from Phase 1 to Phase 2 (Agentic Architecture), showcasing both Production (Docker) and Development (IDE) workflows.

**Note:** This script file is ignored by git (`.gitignore`) so it won't clutter the repo.

---

## 🎬 Scene 1: Introduction & New Documentation

**Action:**

1. Open VS Code.
2. Open `PHASE2_UPGRADE_GUIDE.md`.
3. Scroll through the headers.

**Voiceover:**
"Welcome to the Phase 2 delivery. We have prepared a comprehensive `PHASE2_UPGRADE_GUIDE.md` which serves as your primary manual. It covers everything from stopping your old containers, pulling the new agentic branch, to setting up your local IDE environment for development."

---

## 🎬 Scene 2: The "Hybrid" Architecture

**Action:**

1. Scroll to **"Step 2: Set Up Local Development Environment"** in the guide.
2. Scroll to **"Advanced: Local Development (Hybrid Workflow)"**.

**Voiceover:**
"A key feature of Phase 2 is flexibility. While production runs on strictly containerized Docker services, we've enabled a 'Hybrid Mode' for developers. The guide details how to run the backend agents locally in your IDE (using `uvicorn`) while keeping the heavy database services in Docker. This gives you instant code feedback without rebuilding containers."

---

## 🎬 Scene 3: The Codebase & Agents

**Action:**

1. Open `services/backend/agents/orchestrator.py`.
2. Show the `run_analysis` method.
3. Open `services/backend/rag/rag_manager.py`.

**Voiceover:**
"Under the hood, the system is now driven by this **Orchestrator**. It coordinates specialized agents—Visual Proctor, Code Reviewer, and Integrity Auditor.
And crucially, here is the RAG Manager. Phase 2 introduces a persistent vector database to store 'Ideal Solutions', ensuring that grading is grounded in factual references."

---

## 🎬 Scene 4: Deployment (The Happy Path)

**Action:**

1. Open Integrated Terminal.
2. Run: `docker-compose up --build -d`.
3. Wait for logs: `✔ Container exam-flow-backend-1  Started`.

**Voiceover:**
"For deployment, we follow the 'Critical' step 4 in the guide: a full Docker rebuild. This ensures the new dependencies—like ChromaDB and the headless OpenCV proctor—are correctly installed."

**Action:**
4.  Run: `docker exec exam-flow-backend-1 python init_rag.py`.

**Voiceover:**
"And finally, we initialize the Expert Knowledge Base. This one-time command populates the vector database with our gold-standard examples."

---

## 🎬 Scene 5: Feature Demo - "Solution Package" (ZIP)

**Action:**

1. Open browser (`http://localhost:8501`).
2. Upload `case1_standard_success.zip`.
3. Click **Analyze**.
4. Show resulting breakdown: Technical Score, Management Score, Integrity Status.

**Voiceover:**
"Let's see it in action. The new 'Solution Package' upload processes video, code, and context simultaneously.
...
The result is a holistic evaluation. The Integrity Status is 'Certified', meaning the Visual Proctor confirmed the candidate's presence throughout the exam."

---

## 🎬 Scene 6: Feature Demo - "Single Video" (Restored)

**Action:**

1. Select **"Single Video"** mode.
2. Upload `Java_Demo_Exam-Flow.mp4`.
3. Show the result (likely 20/100 Flagged).

**Voiceover:**
"We've also restored the 'Single Video' upload for backwards compatibility. In this mode, the Code Reviewer switches to 'Visual Analysis'—OCR-reading code from the screen.
However, notice the strictness: because this demo video shows code appearing instantly (pasting), the system correctly flags it as 'Sudden Logic' and caps the score. This proves the new integrity engine is active and rigorous."

---

## 🎬 Scene 7: Conclusion

**Action:**

1. Return to `PHASE2_UPGRADE_GUIDE.md`.

**Voiceover:**
"Everything you see here—the agentic backend, the RAG database, and the hybrid dev tools—is documented and ready in the repository. You can proceed with the upgrade immediately."
