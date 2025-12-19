#!/bin/bash

# InclusiveAI Setup Script
# This script sets up the development environment

echo "🚀 Setting up InclusiveAI project..."

# Frontend setup
echo "📦 Setting up frontend..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
fi
cd ..

# Backend setup
echo "🐍 Setting up backend..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
cd ..

# AI Models setup
echo "🤖 Setting up AI models..."
cd ai_models
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
cd ..

echo "✅ Setup complete!"
echo ""
echo "To start the project:"
echo "  Frontend: cd frontend && npm run dev"
echo "  Backend: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"

