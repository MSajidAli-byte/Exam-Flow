#!/bin/bash
echo ""
echo " ============================================="
echo "   Exam-Flow | Upgrading to Phase 2 (RAG)"
echo " ============================================="
echo ""

echo " [1/5] Stopping current containers..."
docker-compose down
echo ""

echo " [2/5] Switching to Phase 2 branch..."
git fetch origin
git checkout feature/phase2-agentic-rag
git pull origin feature/phase2-agentic-rag
echo ""

echo " [3/5] Enabling Agentic Mode in .env..."
sed -i 's/AGENTIC_MODE=off/AGENTIC_MODE=on/g' .env
echo ""

echo " [4/5] Building Phase 2 containers (first run takes 2-5 min)..."
docker-compose up -d --build
echo ""

echo " [5/5] Initializing RAG Knowledge Base..."
sleep 10
docker exec exam-flow-backend-1 python init_rag.py
echo ""

echo " ============================================="
echo "   Phase 2 running at: http://localhost:8501"
echo "   API Docs at:         http://localhost:8000/docs"
echo " ============================================="
echo ""
read -p "Press [Enter] to close..."
