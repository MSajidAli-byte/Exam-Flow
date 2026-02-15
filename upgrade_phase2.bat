@echo off
echo 🚀 UPGRADING TO EXAM-FLOW PHASE 2...
echo.

echo 🛑 Stopping Phase 1 Services...
docker-compose down

echo.
echo ⚙️  Ensuring Phase 2 Environment...
rem Check if .env exists, if not copy example
if not exist .env copy .env.example .env
find /c "PHASE=2" .env > nul | find /c "0" > nul && echo PHASE=2>>.env
find /c "AGENTIC_MODE=on" .env > nul | find /c "0" > nul && echo AGENTIC_MODE=on>>.env

echo 🔑 REMINDER: Edit .env to add your GOOGLE_API_KEY if missing!
echo.
pause

echo 🏗️  Building Container Images (This may take a moment)...
docker-compose up --build -d

echo.
echo ⏳ Waiting for backend to start (10s)...
timeout /t 10 /nobreak > nul

echo.
echo 🧠 Initializing RAG Knowledge Base...
docker exec exam-flow-backend-1 python init_rag.py

echo.
echo ✅ UPGRADE COMPLETE!
echo Access the application at: http://localhost:8501
echo To verify database: docker exec exam-flow-backend-1 python check_rag_db.py
pause
