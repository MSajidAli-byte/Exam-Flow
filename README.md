# Exam-Flow 🎓

A dockerized microservices suite for automated video grading and proctoring. Features multimodal AI analysis for Java, Docker, and DevOps practical assessments using FastAPI and Gemini 2.0 Flash.

## 🎥 Video Demo

Watch the full walkthrough: [Demo Video](./Video%20Demo/demo%20video_Exam-Flow-hevc.mp4)

## 🏗️ Architecture

- **Backend (FastAPI):** Orchestrates AI analysis, video processing (OpenCV), and Gemini API calls.
- **Frontend (Streamlit):** Student/Admin dashboard for uploading recordings and viewing grading reports.
- **Docker:** Entire suite is containerized for seamless deployment.

## 🚀 Quick Start

### 1. Prerequisites

- Docker & Docker Compose installed.
- Google AI (Gemini) API Key.

### 2. Configuration

Create a `.env` file in the root directory:

```bash
# Example command
cp .env.example .env
```

Edit `.env` and add your `GOOGLE_API_KEY`.

### 3. Run the Suite

```bash
docker compose up --build
```

- **Frontend:** <http://localhost:8501>
- **Backend API:** <http://localhost:8000>

### 4. Manual Setup (Without Docker)

1. **Create Virtual Environment:**

   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate # Linux/Mac
   ```

2. **Install & Run Services:**

   ```bash
   # Terminal 1: Backend
   cd services/backend && pip install -r requirements.txt
   uvicorn main:app --reload --port 8000
   ```

   ```bash
   # Terminal 2: Frontend
   cd services/frontend && pip install -r requirements.txt
   streamlit run app.py
   ```

> **Note:** For manual setup (non-Docker), you must have **FFmpeg** installed on your system path for video analysis to function.

## 📂 Project Structure

- `services/backend`: FastAPI application and AI logic (ai_grader.py, proctor.py).
- `services/frontend`: Streamlit dashboard and PDF generation.
- `docker-compose.yml`: Multi-container orchestration.

## 🛠️ Key Features

- [x] **Gemini 3 Flash Integration**: Cutting-edge reasoning with Gemini 3 Flash Preview.
- [x] **Hardened Integrity Logic**: Zero-tolerance scoring (20/100 cap) for plagiarism.
- [x] **Behavioral Proctoring**: OpenCV-based gaze and face detection (Eyeglasses supported).
- [x] **Hybrid Review Panel**: Manual score overrides with reviewer justification.
- [x] **Professional Reporting**: High-quality PDF assessment exports.
- [x] **Multi-Format Support**: MP4, MOV, AVI, WebM, MKV, FLV video uploads.

## 📚 Documentation

### Core Documentation

- **[CLIENT_HANDOVER.md](CLIENT_HANDOVER.md)** - Client deployment guide and feature overview
- **[BACKEND_ARCHITECTURE.md](BACKEND_ARCHITECTURE.md)** - Detailed backend flow charts and architecture
- **[COST_ANALYSIS.md](COST_ANALYSIS.md)** - API costs, pricing, and quota management

### Phase 2 Development (Agentic AI & RAG)

- **[PHASE2_SETUP_COMPLETE.md](PHASE2_SETUP_COMPLETE.md)** - ⭐ Start here for Phase 2 overview
- **[PHASE2_TRANSITION_GUIDE.md](PHASE2_TRANSITION_GUIDE.md)** - Comprehensive transition guide
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Essential commands cheat sheet

### Version Control

- **Current Stable**: `v1.0-milestone1` (Milestone 1 - Client Approved)
- **Development Branch**: `feature/phase2-agentic-rag` (Phase 2 - Agentic AI)

---

*For detailed client documentation, see [CLIENT_HANDOVER.md](CLIENT_HANDOVER.md)*
*For Phase 2 development, see [PHASE2_SETUP_COMPLETE.md](PHASE2_SETUP_COMPLETE.md)*
