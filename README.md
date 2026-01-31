# Exam-Flow 🎓

A dockerized microservices suite for automated video grading and proctoring. Features multimodal AI analysis for Java, Docker, and DevOps practical assessments using FastAPI and Gemini 1.5 Pro.

## 🏗️ Architecture

- **Backend (FastAPI):** Orchestrates AI analysis, video processing (MediaPipe), and Gemini API calls.
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

## 📂 Project Structure

- `services/backend`: FastAPI application and AI logic.
- `services/frontend`: Streamlit dashboard.
- `docker-compose.yml`: Multi-container orchestration.

## 🛠️ Features (In Development)

- [ ] Gemini 1.5 Pro Multimodal Pipeline.
- [ ] Behavioral Proctoring (MediaPipe).
- [ ] Automated Technical Grading (Java/Docker/DevOps).
- [ ] PDF Report Generation.
