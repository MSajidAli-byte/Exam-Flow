@echo off
title Exam-Flow: Roll Back to Phase 1
color 0E
echo.
echo  =============================================
echo    Exam-Flow ^| Rolling Back to Phase 1
echo  =============================================
echo.

echo  [1/4] Stopping Phase 2 containers...
docker-compose down
echo.

echo  [2/4] Switching to Phase 1 branch (main)...
git fetch origin
git checkout main
git pull origin main
echo.

echo  [3/4] Disabling Agentic Mode in .env...
powershell -Command "(Get-Content .env) -replace 'AGENTIC_MODE=on','AGENTIC_MODE=off' | Set-Content .env"
echo.

echo  [4/4] Starting Phase 1 containers...
echo        (Uses cached Docker image - no rebuild needed)
docker-compose up -d
echo.

echo  =============================================
echo    Phase 1 running at: http://localhost:8501
echo    No RAG setup needed for Phase 1.
echo  =============================================
echo.
pause
