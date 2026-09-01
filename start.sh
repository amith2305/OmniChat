#!/bin/bash
# OmniChat AI - Unix/Linux/macOS Startup Script

echo "========================================"
echo "  OmniChat AI - Multimodal RAG Assistant"
echo "========================================"
echo ""

# Check if .env exists
if [ ! -f backend/.env ]; then
    echo "[ERROR] .env file not found!"
    echo "Please copy backend/.env.example to backend/.env and configure it."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d backend/.venv ]; then
    echo "[ERROR] Virtual environment not found!"
    echo "Please run: cd backend && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Check if Ollama is running
echo "[1/3] Checking Ollama service..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "[WARNING] Ollama is not running or not accessible at http://localhost:11434"
    echo "Please start Ollama before continuing."
    read -p "Press Enter to continue anyway or Ctrl+C to exit..."
fi

# Activate virtual environment and start backend
echo "[2/3] Starting FastAPI backend..."
cd backend
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait a moment for the server to start
sleep 3

# Open browser (platform-specific)
echo "[3/3] Opening browser..."
if command -v xdg-open > /dev/null; then
    xdg-open http://localhost:8000
elif command -v open > /dev/null; then
    open http://localhost:8000
else
    echo "Please open http://localhost:8000 in your browser"
fi

echo ""
echo "========================================"
echo "  OmniChat AI is running!"
echo "========================================"
echo "  Backend API: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server."
echo ""

# Wait for Ctrl+C
trap "kill $BACKEND_PID 2>/dev/null; exit" INT
wait $BACKEND_PID
