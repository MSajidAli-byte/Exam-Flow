# Exam-Flow Manual (Simplified)

## 1. Installation & Upgrade

**Windows:**
Double-click `upgrade_phase2.bat`.

**Linux / Mac:**

```bash
./upgrade_phase2.sh
```

**This script automatically:**

1. Stops old Phase 1 containers.
2. Checks out the `feature/phase2-agentic-rag` branch.
3. Builds the new Docker images.
4. Initializes the RAG database with "Idea Solutions".

---

## 2. Using the System

**URL:** `http://localhost:8501`

**A. Upload Mode: "Solution Package (ZIP)"**
Select this for full grading.

- **Upload:** A standard .zip file containing your project.
- **Context:** Paste exam instructions in the "Exam Context / Instructions" text box in the UI.
- **Result:** You will get a Technical Score, Integrity Check, and PDF Report.

**B. Upload Mode: "Single Video"**
Select this for video-only submissions.

- **Action:** AI reads code from the screen using OCR.
- **Warning:** Code that appears instantly (pasting) is flagged as "Sudden Logic" (Score Cap: 20/100).

---

## 3. Supported Files (Inside the ZIP)

The system automatically scans subfolders. No strict structure required.

| File Type | Extensions Supported | Notes |
| :--- | :--- | :--- |
| **Code** | `.java`, `.py`, `.js`, `.cpp`, `.cs`, `.go`, `.ts` | Analyzes logic & syntax. Multi-file support enabled. |
| **Video** | `.mp4`, `.mov`, `.avi`, `.mkv` | Used for behavioral proctoring (gaze/face). |
| **Docs** | `.txt`, `.md`, `.yaml` | Read as additional context (e.g. README). |

*Note: PDF/Word files are currently ignored.*

---

## 4. Troubleshooting

**"ChromaDB folder is empty?"**
Normal. Data lives inside the hidden Docker Volume.
To verify data exists, run:

```bash
docker exec exam-flow-backend-1 python check_rag_db.py
```
