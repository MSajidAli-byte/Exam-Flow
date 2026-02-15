# Exam-Flow Phase 2: Agentic Multi-Modal Assessment 🎓

Welcome to the **Agentic Phase 2** release. This version transforms the platform from a linear grader into a robust multi-agent system with RAG (Retrieval Augmented Generation) for factual grading.

---

## 🚀 One-Click Upgrade (Start Here)

We have automated the entire transition process. Run the script for your OS:

### **Windows**

Double-click `upgrade_phase2.bat` or run in terminal:

```cmd
.\upgrade_phase2.bat
```

### **Linux / Mac**

```bash
chmod +x upgrade_phase2.sh
./upgrade_phase2.sh
```

**What this script does:**

1. Stops old Phase 1 containers.
2. Updates your `.env` for Agentic Mode.
3. Rebuilds the system with new dependencies (ChromaDB, OpenCV Headless).
4. Initializes the Expert Knowledge Base (RAG).

---

## 📂 Documentation

Full documentation has been organized into the `docs/` folder:

- **[PHASE2_UPGRADE_GUIDE.md](docs/PHASE2_UPGRADE_GUIDE.md)**: Detailed step-by-step manual upgrade instructions.
- **[PHASE2_CLIENT_HANDOVER.md](docs/PHASE2_CLIENT_HANDOVER.md)**: Feature overview for the client.
- **[RESEARCH_PAPER_STRUCTURE.md](docs/RESEARCH_PAPER_STRUCTURE.md)**: Blueprint for academic publication (No humans required).
- **[PHASE2_RESEARCH_PROTOCOL.md](docs/PHASE2_RESEARCH_PROTOCOL.md)**: Scientific validation metrics.

---

## 🏗️ Architecture Visualization

The new system orchestrated by 4 specialized AI Agents:

1. **Visual Proctor Agent**: Analyzes behavioral video (Gaze/Face detection).
2. **Code Reviewer Agent**: Grades syntax & logic (Text or Video OCR).
3. **Integrity Auditor Agent**: Cross-references behavior with code timeline.
4. **Final Grader Agent**: Synthesizes all reports into a final verdict.

---

## 🛠️ Advanced: Manual Developer Setup

If you prefer to run services locally (Hybrid Mode) instead of Docker:

1. **Backend**: `cd services/backend && uvicorn main:app --reload`
2. **Frontend**: `cd services/frontend && streamlit run app.py`

*See `docs/PHASE2_UPGRADE_GUIDE.md` for full local setup details.*
