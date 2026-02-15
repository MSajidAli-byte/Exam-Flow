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
AGENTIC_MODE=on
# Optional: Set a password for the UI (Default: examflow2026)
APP_PASSWORD=your_secure_password
```

*Note: Phase 1 worked without `PHASE=2`, but Phase 2 requires it to activate the Orchestrator.*

---

## 💻 Step 3: Set Up Local Development Environment (IDE)

Even if you run the application via Docker, setting up a local environment ensures your IDE (VS Code, PyCharm) can provide code completion and debugging support.

### **1. Create & Activate Virtual Environment**

Open your terminal in the project root:

**Windows:**

```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### **2. Install Backend Dependencies**

```bash
cd services/backend
pip install -r requirements.txt
```

### **3. Install Frontend Dependencies**

```bash
cd ../frontend
pip install -r requirements.txt
```

*Return to the project root before proceeding:*

```bash
cd ../..
```

---

## 🏗️ Step 4: Rebuild & Launch (CRITICAL)

Phase 2 adds new system dependencies (ChromaDB, Vector Storage). You **MUST** rebuild the containers, or the upgrade will fail.

```bash
# Force a rebuild of the backend and frontend
docker-compose up --build -d
```

Wait until you see:
`✔ Container exam-flow-backend-1  Started`
`✔ Container exam-flow-frontend-1  Started`

---

## 🧠 Step 5: Initialize the Expert Knowledge Base (RAG)

The new AI agents need a database of "Ideal Solutions" to grade against. We've included a script to populate this automatically.

Run this command **once** after the containers are running:

```bash
docker exec exam-flow-backend-1 python init_rag.py
```

**Expected Output:**

```text
Initialize Ideal Solution Library...
Added solution java_oop_001 to library.
Added solution docker_001 to library.
...
Library initialized successfully.
```

---

## �️ Advanced: Local Development (Hybrid Workflow)

If you want to edit code and see changes instantly without rebuilding Docker containers, follow this **Hybrid Workflow**:

### **1. Stop Docker Containers**

Available ports (8000, 8501) must be free.

```bash
docker-compose down
```

### **2. Run Backend Locally (with Auto-Reload)**

Navigate to the backend folder and start the server:

```bash
cd services/backend
# Ensure venv is active
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

*Now you can edit `orchestrator.py` or agent logic and the server will restart automatically!*

### **3. Run Frontend Locally**

Open a new terminal, navigate to frontend, and launch:

```bash
cd services/frontend
# Ensure venv is active
streamlit run app.py --server.port 8501
```

### **Note on Data Persistence**

When running locally, the **RAG Database** (`chroma_db`) and **Uploads** (`uploads`) will be created inside your local `services/backend/` directory.

- **Docker:** Stores data in Docker Volumes.
- **Local:** Stores data in local folders.
*If you switch between methods, you may need to re-initialize the RAG library.*

---

## �🚀 Step 6: Verify Installation

1. Go to `http://localhost:8501`.
2. You should see the new **"Solution Package (ZIP)"** upload option.
3. The sidebar should show **"Phase 2: Agentic Mode Active"**.

You are now running the full Phase 2 architecture!
