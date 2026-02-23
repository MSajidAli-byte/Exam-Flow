@echo off
echo ============================================
echo   Exam-Flow: Roll Back to Phase 1
echo ============================================

echo.
echo [1/4] Stopping Phase 2 containers...
docker-compose down

echo.
echo [2/4] Switching to Phase 1 branch (main)...
git fetch origin
git checkout main
git pull origin main

echo.
echo [3/4] Disabling Phase 2 environment flags...
powershell -Command "(Get-Content .env) -replace 'PHASE=2','PHASE=1' | Set-Content .env"
powershell -Command "(Get-Content .env) -replace 'AGENTIC_MODE=on','AGENTIC_MODE=off' | Set-Content .env"

echo.
echo [4/4] Starting Phase 1 containers...
echo       (Uses cached image if available — no full rebuild needed)
docker-compose up -d
echo.
echo ============================================
echo   Phase 1 is running at http://localhost:8501
echo   No RAG initialization needed for Phase 1.
echo ============================================
