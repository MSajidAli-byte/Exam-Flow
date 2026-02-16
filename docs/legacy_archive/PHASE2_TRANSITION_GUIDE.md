# Phase 2 Transition Guide: Agentic AI & RAG System

## Overview

This guide covers the transition from **Milestone 1 (Core AI Grading)** to **Milestone 2 (Agentic AI with RAG)** while maintaining the ability to rollback to the stable version.

---

## Pre-Transition Checklist

### ✅ Completed Steps

- [x] Git tag created: `v1.0-milestone1`
- [x] Dependencies frozen: `requirements_m1_stable.txt`
- [x] Docker volumes configured for data persistence
- [x] Environment variables added for phase control

### 🔄 Pending Steps (Execute when Docker is running)

- [ ] Tag Docker images for Milestone 1
- [ ] Create Phase 2 development branch
- [ ] Install new dependencies (langchain, chromadb)
- [ ] Test rollback procedure

---

## Docker Image Backup (When Docker Desktop is Running)

### Step 1: Tag Current Stable Images

```bash
# Tag backend image
docker tag exam-flow-backend:latest exam-flow-backend:v1.0-milestone1

# Tag frontend image  
docker tag exam-flow-frontend:latest exam-flow-frontend:v1.0-milestone1

# Verify tags were created
docker images | grep exam-flow
```

### Step 2: Save Images to Disk (Optional Backup)

```bash
# Save backend image
docker save exam-flow-backend:v1.0-milestone1 -o exam-flow-backend-v1.0.tar

# Save frontend image
docker save exam-flow-frontend:v1.0-milestone1 -o exam-flow-frontend-v1.0.tar

# Store these .tar files in a safe location (external drive, cloud storage)
```

---

## Git Workflow for Phase 2

### Step 1: Ensure Main Branch is Clean

```bash
# Check current status
git status

# Commit any pending changes
git add .
git commit -m "chore: prepare for Phase 2 transition"
git push origin main
```

### Step 2: Create Phase 2 Development Branch

```bash
# Create and switch to Phase 2 branch
git checkout -b feature/phase2-agentic-rag

# Push to remote
git push -u origin feature/phase2-agentic-rag
```

### Step 3: Create Git Tag for Milestone 1

```bash
# Tag the stable release
git tag -a v1.0-milestone1 -m "Milestone 1: Core AI Grading & Proctoring - Client Approved & Paid"

# Push tag to GitHub
git push origin v1.0-milestone1
```

---

## Phase 2 Dependencies

### New Libraries to Add

Add these to `services/backend/requirements.txt`:

```txt
# Phase 2: Agentic AI & RAG Dependencies
langchain==0.1.0
langchain-google-genai==0.0.6
chromadb==0.4.22
sentence-transformers==2.3.1
tiktoken==0.5.2

# Optional: Enhanced features
pydantic==2.5.3
tenacity==8.2.3
```

### Installation Command

```bash
# From project root, rebuild containers with new dependencies
docker-compose down
docker-compose up --build -d

# This will take longer due to ChromaDB's C++ dependencies
```

---

## Docker Volume Management

### Understanding the New Volumes

Your updated `docker-compose.yml` now includes:

1. **`chroma_db`**: Stores the vector database for RAG
   - Contains embeddings of "ideal solutions"
   - Persists across container restarts
   - Location: Docker managed volume

2. **`uploads`**: Stores uploaded exam videos
   - Prevents data loss on container rebuild
   - Accessible for analysis and archiving

### Volume Commands

```bash
# List all volumes
docker volume ls

# Inspect ChromaDB volume
docker volume inspect exam-flow_chroma_db

# Backup ChromaDB volume (important for research data)
docker run --rm -v exam-flow_chroma_db:/data -v $(pwd):/backup alpine tar czf /backup/chroma_backup.tar.gz -C /data .

# Restore ChromaDB volume (if needed)
docker run --rm -v exam-flow_chroma_db:/data -v $(pwd):/backup alpine tar xzf /backup/chroma_backup.tar.gz -C /data
```

---

## Environment Variables for Phase Control

### Phase 1 (Stable - Current Production)

```bash
# .env file
GOOGLE_API_KEY=your_key_here
PHASE=1
AGENTIC_MODE=off
```

### Phase 2 (Development - Agentic AI)

```bash
# .env file
GOOGLE_API_KEY=your_key_here
PHASE=2
AGENTIC_MODE=on
```

### Switching Between Phases

```bash
# Test Phase 2 features
echo "PHASE=2" >> .env
echo "AGENTIC_MODE=on" >> .env
docker-compose restart

# Rollback to Phase 1
echo "PHASE=1" > .env
echo "AGENTIC_MODE=off" >> .env
docker-compose restart
```

---

## Rollback Procedures

### Quick Rollback (Git)

```bash
# Return to Milestone 1 code
git checkout v1.0-milestone1

# Rebuild containers with stable code
docker-compose up --build -d
```

### Full Rollback (Git + Docker)

```bash
# Switch to main branch
git checkout main

# Use tagged Docker images
docker-compose down
docker tag exam-flow-backend:v1.0-milestone1 exam-flow-backend:latest
docker tag exam-flow-frontend:v1.0-milestone1 exam-flow-frontend:latest
docker-compose up -d
```

### Emergency Rollback (Restore from Disk)

```bash
# Load saved images
docker load -i exam-flow-backend-v1.0.tar
docker load -i exam-flow-frontend-v1.0.tar

# Start containers
docker-compose up -d
```

---

## Testing Strategy

### Phase 1 Regression Tests

Before deploying Phase 2, ensure Phase 1 still works:

```bash
# Switch to Phase 1 mode
export PHASE=1
export AGENTIC_MODE=off

# Test core features
# 1. Upload a test video
# 2. Verify proctoring analysis works
# 3. Check PDF report generation
# 4. Validate custom rubric handling
```

### Phase 2 Feature Tests

```bash
# Switch to Phase 2 mode
export PHASE=2
export AGENTIC_MODE=on

# Test new features
# 1. Upload ideal solution
# 2. Verify RAG retrieval
# 3. Test agentic reasoning
# 4. Compare with Phase 1 results
```

---

## Data Migration Plan

### Ideal Solutions Library

For Phase 2, you'll need to populate ChromaDB with ideal solutions:

```python
# Example structure (to be implemented)
ideal_solutions = {
    "java_oop": {
        "code": "...",
        "explanation": "...",
        "rubric_score": 95
    },
    "docker_deployment": {
        "code": "...",
        "explanation": "...",
        "rubric_score": 90
    }
}
```

### Migration Script Location

Create: `services/backend/migrate_to_phase2.py`

---

## Client Communication Template

### Message to Motasem

```
Hi Motasem,

Great news! Milestone 1 is now safely archived and we're ready to begin Phase 2 (Agentic AI).

**What I've Set Up:**

1. **Stable Backup**: Created permanent snapshot (v1.0-milestone1) of the working system
2. **Data Persistence**: Added Docker volumes so your "Ideal Solutions" library will be permanent
3. **Phase Toggle**: You can switch between Phase 1 (stable) and Phase 2 (experimental) instantly
4. **Rollback Safety**: If anything breaks, we can return to the paid version in under 60 seconds

**Next Steps:**

1. I'll create a development branch for Phase 2 features
2. Install the new AI libraries (langchain, chromadb)
3. Build the "Ideal Solutions" ingestion system
4. Test the agentic reasoning against Phase 1 baseline

**Timeline:**
- Week 1: RAG system setup + ideal solutions library
- Week 2: Agentic AI integration + testing
- Week 3: Comparative analysis (Phase 1 vs Phase 2)
- Week 4: Research data collection + documentation

I'll keep you updated on progress. The current system remains fully operational during development.

Best regards,
Mohammad
```

---

## Research Baseline Metrics (For Academic Paper)

### Phase 1 Metrics to Capture

Before starting Phase 2, document these for comparison:

```python
baseline_metrics = {
    "accuracy": {
        "plagiarism_detection": "X%",
        "technical_grading": "X%",
        "false_positive_rate": "X%"
    },
    "performance": {
        "avg_analysis_time": "X seconds",
        "cost_per_video": "$X",
        "model_used": "gemini-3-flash-preview"
    },
    "user_satisfaction": {
        "grading_fairness": "X/10",
        "report_clarity": "X/10"
    }
}
```

### Phase 2 Comparison Points

- Improvement in technical accuracy
- Reduction in false positives
- Enhanced explanation quality
- Cost efficiency (if using smaller models for RAG)

---

## Troubleshooting

### Issue: ChromaDB Build Fails

**Solution**: Ensure you have build tools installed

```bash
# Windows (in PowerShell as Admin)
choco install visualstudio2019buildtools

# Or use a pre-built ChromaDB Docker image
```

### Issue: Volume Permissions Error

**Solution**: Reset volume permissions

```bash
docker-compose down -v
docker volume rm exam-flow_chroma_db
docker-compose up -d
```

### Issue: Phase Toggle Not Working

**Solution**: Verify environment variables

```bash
# Check current env vars
docker-compose config

# Force rebuild
docker-compose up --build --force-recreate
```

---

## Summary

✅ **Milestone 1 is Safe**: Tagged in Git and Docker  
✅ **Data is Persistent**: ChromaDB and uploads won't be lost  
✅ **Rollback is Easy**: Multiple recovery options available  
✅ **Phase Control**: Can toggle between stable and experimental  

**You are now ready to begin Phase 2 development!**

---

**Last Updated**: February 12, 2026  
**Status**: Ready for Phase 2 Development  
**Stable Version**: v1.0-milestone1
