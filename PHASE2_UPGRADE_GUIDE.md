# 🚀 Phase 2 Upgrade Guide: From Prototype to Agentic AI

This guide is specifically for upgrading an existing "Phase 1" installation to the new **Phase 2 Agentic Architecture**.

## ✅ Prerequisites

- You must have the previous Phase 1 version running or installed.
- Ensure Docker Desktop is running.

---

## 📦 Step 1: Switch to the New Branch

Stop your currently running application first:

```bash
docker-compose down
```

Now, pull the latest changes and switch to the Phase 2 branch:

```bash
git fetch origin
git checkout feature/phase2-agentic-rag
git pull origin feature/phase2-agentic-rag
```

---

## ⚙️ Step 2: Configure Environment

Open your `.env` file (create one if missing) and ensure these lines are set. Phase 2 introduces `AGENTIC_MODE` and persistent storage.

```ini
# .env file
GOOGLE_API_KEY=your_gemini_api_key_here
PHASE=2
AGENTIC_MODE=on
```

*Note: Phase 1 worked without `PHASE=2`, but Phase 2 requires it to activate the Orchestrator.*

---

## 🏗️ Step 3: Rebuild & Launch (CRITICAL)

Phase 2 adds new system dependencies (ChromaDB, Vector Storage). You **MUST** rebuild the containers, or the upgrade will fail.

```bash
# Force a rebuild of the backend and frontend
docker-compose up --build -d
```

Wait until you see:
`✔ Container exam-flow-backend-1  Started`
`✔ Container exam-flow-frontend-1  Started`

---

## 🧠 Step 4: Initialize the Expert Knowledge Base (RAG)

The new AI agents need a database of "Ideal Solutions" to grade against. We've included a script to populate this automatically.

Run this command **once** after the containers are running:

```bash
docker exec exam-flow-backend-1 python init_rag.py
```

**Expected Output:**

```
Initialize Ideal Solution Library...
Added solution java_oop_001 to library.
Added solution docker_001 to library.
...
Library initialized successfully.
```

---

## 🚀 Step 5: Verify Installation

1. Go to `http://localhost:8501`.
2. You should see the new **"Solution Package (ZIP)"** upload option.
3. The sidebar should show **"Phase 2: Agentic Mode Active"**.

You are now running the full Phase 2 architecture!
