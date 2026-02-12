# Exam-Flow Phase 2: Agentic Multi-Modal & RAG (Client Handover)

This update transitions the platform from a linear AI grading system (Milestone 1) to an **Agentic Multi-Modal System** (Phase 2). It features an expert team of AI agents and a persistent "Ideal Solution Library" (RAG).

## 🚀 How to Move to the New Version

To use the Phase 2 features, please follow these steps:

### 1. Update the Repository

Ensure you are on the correct branch:

```bash
git fetch
git checkout feature/phase2-agentic-rag
git pull origin feature/phase2-agentic-rag
```

### 2. Update Environment Variables (.env)

Your `.env` file needs two new flags to activate Phase 2:

```ini
PHASE=2
AGENTIC_MODE=on
# Optional: Set a password for the UI (Default: examflow2026)
APP_PASSWORD=your_secure_password 
```

### 3. Restart Docker Containers

Since we added persistent volumes for the Vector Database and Video storage, you must rebuild the containers:

```bash
docker-compose down
docker-compose up --build -d
```

### 4. Initialize the Expert Library (RAG)

You must populate the "Ideal Solution Library" with initial benchmarks. Run this command while the backend is running:

```bash
docker exec exam-flow-backend-1 python init_rag.py
```

*Note: This specific step now uses Gemini Embeddings (`gemini-embedding-001`) to ensure fast initialization without downloading local models.*

---

## 🛠️ Key Technical Changes

### **Docker Infrastructure**

* **Persistent Volumes**: Data is no longer lost on container restart.
  * `chroma_db`: Stores your expert solutions.
  * `uploads`: Stores candidate videos.
* **Multi-Agent Mode**: Setting `AGENTIC_MODE=on` routes analysis to a team of 4 specialized agents (Visual Proctor, Code Reviewer, Integrity Auditor, Final Grader).

### **New Upload Strategy: "Solution Package" (ZIP)**

Instead of just a video, you can now upload a **ZIP** file containing:

1. The Candidate's Video (.mp4)
2. The Solution Source Code (.java, .py, etc.)
3. An optional `context.txt` (Providing specific exam instructions).

### **Research-First Logging**

The backend now captures:
* **Agent Confidence Scores** (For validity studies).
* **Integrity Audit Logs** (Flagging "Sudden Logic" while the candidate's face was missing).

---

## ✅ Rollback Procedure

If you need to return to the stable Milestone 1 version for any reason:

1. Check out `main` or use the tag `v1.0-milestone1`.
2. Set `PHASE=1` and `AGENTIC_MODE=off` in your `.env`.
3. Restart Docker: `docker-compose up -d`.
