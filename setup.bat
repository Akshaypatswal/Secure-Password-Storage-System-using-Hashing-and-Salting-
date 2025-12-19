@echo off

REM InclusiveAI Setup Script for Windows
REM This script sets up the development environment

echo Setting up InclusiveAI project...

REM Frontend setup
echo Setting up frontend...
cd frontend
if not exist "node_modules" (
    call npm install
)
cd ..

REM Backend setup
echo Setting up backend...
cd backend
if not exist "venv" (
    python -m venv venv
)
call venv\Scripts\activate
pip install -r requirements.txt
cd ..

REM AI Models setup
echo Setting up AI models...
cd ai_models
if not exist "venv" (
    python -m venv venv
)
call venv\Scripts\activate
pip install -r requirements.txt
cd ..

echo Setup complete!
echo.
echo To start the project:
echo   Frontend: cd frontend ^&^& npm run dev
echo   Backend: cd backend ^&^& venv\Scripts\activate ^&^& uvicorn app.main:app --reload

