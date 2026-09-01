@echo off
REM OmniChat AI - Windows Startup Script

echo ========================================
echo   OmniChat AI - Multimodal RAG Assistant
echo ========================================
echo.

REM Check if .env exists
if not exist backend\.env (
    echo [ERROR] .env file not found!
    echo Please copy backend\.env.example to backend\.env and configure it.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist backend\.venv (
    echo [ERROR] Virtual environment not found!
    echo Please run: cd backend ^&^& python -m venv .venv ^&^& .venv\Scripts\activate ^&^& pip install -r requirements.txt
    pause
    exit /b 1
)

REM Check if Ollama is running
echo [1/3] Checking Ollama service...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Ollama is not running or not accessible at http://localhost:11434
    echo Please start Ollama before continuing.
    pause
)

REM Activate virtual environment and start backend
echo [2/3] Starting FastAPI backend...
cd backend
call .venv\Scripts\activate
start "OmniChat AI Backend" uvicorn app.main:app --host 0.0.0.0 --port 8000

REM Wait a moment for the server to start
timeout /t 3 /nobreak >nul

REM Open browser
echo [3/3] Opening browser...
start http://localhost:8000

echo.
echo ========================================
echo   OmniChat AI is running!
echo ========================================
echo   Backend API: http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C in the backend window to stop the server.
echo.
pause
