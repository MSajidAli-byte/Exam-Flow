# Phase 2 Quick Reference Card

## 🚀 Quick Start Commands

### Start Docker Desktop First

```bash
# Verify Docker is running
docker --version
docker-compose --version
```

---

## 📦 Initial Setup (One-Time)

### 1. Backup Current Stable Version

```bash
# Tag Docker images (run when Docker Desktop is active)
docker tag exam-flow-backend:latest exam-flow-backend:v1.0-milestone1
docker tag exam-flow-frontend:latest exam-flow-frontend:v1.0-milestone1

# Create Git tag
git tag -a v1.0-milestone1 -m "Milestone 1: Client Approved"
git push origin v1.0-milestone1
```

### 2. Create Phase 2 Branch

```bash
git checkout -b feature/phase2-agentic-rag
git push -u origin feature/phase2-agentic-rag
```

---

## 🔄 Daily Workflow

### Switch to Phase 2 Development

```bash
# Edit .env file
PHASE=2
AGENTIC_MODE=on

# Rebuild and restart
docker-compose up --build -d
```

### Test Phase 1 (Stable)

```bash
# Edit .env file
PHASE=1
AGENTIC_MODE=off

# Restart
docker-compose restart
```

---

## 🛠️ Common Operations

### View Logs

```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100 backend
```

### Rebuild After Code Changes

```bash
docker-compose up --build -d
```

### Clean Restart

```bash
docker-compose down
docker-compose up -d
```

### Full Reset (Keeps Volumes)

```bash
docker-compose down
docker-compose up --build --force-recreate -d
```

---

## 💾 Volume Management

### List Volumes

```bash
docker volume ls
```

### Backup ChromaDB

```bash
docker run --rm \
  -v exam-flow_chroma_db:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/chroma_backup_$(date +%Y%m%d).tar.gz -C /data .
```

### Restore ChromaDB

```bash
docker run --rm \
  -v exam-flow_chroma_db:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/chroma_backup_YYYYMMDD.tar.gz -C /data
```

---

## 🔙 Rollback Procedures

### Quick Rollback (Code Only)

```bash
git checkout main
docker-compose restart
```

### Full Rollback (Code + Images)

```bash
git checkout v1.0-milestone1
docker-compose down
docker tag exam-flow-backend:v1.0-milestone1 exam-flow-backend:latest
docker tag exam-flow-frontend:v1.0-milestone1 exam-flow-frontend:latest
docker-compose up -d
```

---

## 🧪 Testing Checklist

### Phase 1 Regression Test

- [ ] Upload MP4 video
- [ ] Verify proctoring analysis
- [ ] Check PDF report generation
- [ ] Test custom rubric
- [ ] Validate WebM support

### Phase 2 Feature Test

- [ ] Upload ideal solution
- [ ] Verify RAG retrieval
- [ ] Test agentic reasoning
- [ ] Compare with Phase 1 results

---

## 🐛 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs backend

# Force rebuild
docker-compose up --build --force-recreate -d
```

### Port Already in Use

```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <PID> /F

# Or change port in docker-compose.yml
```

### Volume Permission Issues

```bash
# Reset volumes
docker-compose down -v
docker volume rm exam-flow_chroma_db
docker-compose up -d
```

---

## 📊 Monitoring

### Check Container Status

```bash
docker-compose ps
```

### Check Resource Usage

```bash
docker stats
```

### Access Container Shell

```bash
# Backend
docker-compose exec backend bash

# Frontend
docker-compose exec frontend bash
```

---

## 🔐 Security Checklist

- [ ] `.env` is in `.gitignore`
- [ ] API keys are not hardcoded
- [ ] Sensitive data is in volumes, not images
- [ ] Docker images are tagged before major changes

---

## 📞 Emergency Contacts

**If something breaks during client demo:**

1. **Immediate Rollback**: `git checkout main && docker-compose restart`
2. **Check Logs**: `docker-compose logs -f backend`
3. **Verify .env**: Ensure `PHASE=1` and `AGENTIC_MODE=off`

---

**Last Updated**: February 12, 2026  
**Current Stable**: v1.0-milestone1  
**Development Branch**: feature/phase2-agentic-rag
