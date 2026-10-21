# Exam-Flow: AI-Powered Assessment & Proctoring 🎓

Two phases. One codebase. Use the scripts below to switch between them.

---

## ⚡ Quick Start

### 🔑 Google Gemini API Key Setup (Required First Step)
> [!IMPORTANT]
> **Before running the application with your API key, you MUST first enable the Gemini API in the Google Cloud Console:**
> 1. Go to the [Google Cloud Console Generative Language API](https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com) and click **Enable**.
> 2. Create or copy your Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
> 3. Add your key to the `.env` file in the project root:
>    ```env
>    GOOGLE_API_KEY=your_api_key_here
>    PHASE=1
>    AGENTIC_MODE=on
>    ```
> *(Without enabling the API in Google Cloud Console, model requests and file uploads will fail with `API_KEY_INVALID` or `400/403` status errors).*

---

### Upgrade to Phase 2 (Agentic + RAG)

**Windows:**

```cmd
.\upgrade_phase2.bat
```

**Linux / Mac:**

```bash
chmod +x upgrade_phase2.sh && ./upgrade_phase2.sh
```

### Roll Back to Phase 1 (Single LLM)

**Windows:**

```cmd
.\rollback_phase1.bat
```

**Linux / Mac:**

```bash
chmod +x rollback_phase1.sh && ./rollback_phase1.sh
```

---

## 🐳 Docker: When to Rebuild?

If you modify **any Python files** (such as the AI Agent prompts in `services/backend/agents/`), you **MUST rebuild** your Docker containers for the changes to take effect.

| Situation | Command |
| :--- | :--- |
| **You edited code (e.g., changed an Agent prompt)** | `docker-compose up -d --build` |
| First time running a phase | `docker-compose up -d --build` |
| Switching back to a phase you've run before | `docker-compose up -d` (uses cached image) |

*Note: The `upgrade_phase2` and `rollback_phase1` scripts handle the build flag automatically when switching branches.*

---

## 🧠 RAG Knowledge Base (Phase 2 Only)

The RAG database stores your "Ideal Solutions." Initialize it once after upgrading to Phase 2.

**Initialize with built-in examples (Java OOP, Docker, Python Factorial):**

```bash
docker exec exam-flow-backend-1 python init_rag.py
```

**Verify the database is populated:**

```bash
docker exec exam-flow-backend-1 python check_rag_db.py
```

**Add a custom solution via API (no restart needed):**

```bash
curl -X POST http://localhost:8000/library/upload \
  -H "Content-Type: application/json" \
  -d '{
    "solution_id": "java_factorial_001",
    "code": "public static int factorial(int n) { return n <= 1 ? 1 : n * factorial(n-1); }",
    "context": "Recursive factorial implementation in Java.",
    "category": "Java"
  }'
```

> **Note:** The RAG database persists in a Docker Volume. Switching branches does not erase it.
> To reset it completely: `docker volume rm exam-flow_chroma_db`

---

## 📂 Documentation

- **[PHASE2_MANUAL.md](docs/PHASE2_MANUAL.md)**: Setup, usage, and supported file types.
- **[WORKFLOW_ARCHITECTURE.md](docs/WORKFLOW_ARCHITECTURE.md)**: How the agents communicate.
- **[RESEARCH_PAPER_STRUCTURE.md](docs/RESEARCH_PAPER_STRUCTURE.md)**: Academic publication blueprint.

---

## 🏗️ Phase 2 Agent Architecture

4 specialized agents orchestrated sequentially:

1. **Visual Proctor** — OpenCV face/gaze detection → LLM behavioral summary
2. **Code Reviewer** — Reads submitted code + watches screen recording simultaneously
3. **Integrity Auditor** — Cross-references screen events, code file, and behavioral flags
4. **Final Grader** — Synthesizes all reports into one verdict with score

---

## 🛠️ Local Development (No Docker)

```bash
# Backend
cd services/backend && uvicorn main:app --reload

# Frontend (separate terminal)
cd services/frontend && streamlit run app.py
```
