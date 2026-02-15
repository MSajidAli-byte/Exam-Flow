#!/bin/bash
echo "🚀 Starting Phase 2 Upgrade Protocol..."

# Step 1: Stop Phase 1 Services
echo "🛑 Stopping existing containers..."
docker-compose down

# Step 1.5: Switch to Phase 2 Branch
echo "🔄 Switching to Phase 2 Code..."
git fetch origin
git checkout feature/phase2-agentic-rag
git pull origin feature/phase2-agentic-rag

# Step 2: Ensure Environment
if [ ! -f .env ]; then
    echo "⚠️  WARNING: .env file missing!"
    echo "Creating from .env.example..."
    cp .env.example .env
    echo "🔑 Please edit .env to add your GOOGLE_API_KEY before proceeding."
    read -p "Press Enter once you have added the API Key..."
fi

# Ensure Phase 2 flags are set
# Appending blindly is risky if duplicate, but simple sed is better.
# For simplicity, we assume .env is clean or just remind user.
echo "⚙️  Configuring Environment for AGENTIC MODE..."
# Simple check if lines exist, append if not
grep -qxF 'PHASE=2' .env || echo 'PHASE=2' >> .env
grep -qxF 'AGENTIC_MODE=on' .env || echo 'AGENTIC_MODE=on' >> .env

# Step 3: Rebuild Containers (Crucial for new dependencies)
echo "🏗️  Building Phase 2 Containers (This may take a moment)..."
docker-compose up --build -d

# Wait for healthy backend
echo "⏳ Waiting for backend to initialize..."
sleep 10  # Give it a moment to start Uvicorn

# Step 4: Initialize Knowledge Base
echo "🧠 Initializing RAG Knowledge Base..."
docker exec exam-flow-backend-1 python init_rag.py

# Step 5: Verify
echo "Example Verification Command:"
echo "docker exec exam-flow-backend-1 python check_rag_db.py"

echo "✅ UPGRADE COMPLETE! Access at http://localhost:8501"
