#!/bin/bash

# CraveLess Quick Start Script

echo "🍽️  CraveLess - AI Food Decision Engine"
echo "========================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    exit 1
fi

# Check Node
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 16+"
    exit 1
fi

echo "✅ Python $(python3 --version)"
echo "✅ Node $(node --version)"
echo ""

# Backend setup
echo "📦 Setting up backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "  Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo "  Installing dependencies..."
pip install -q -r requirements.txt

# Initialize database
echo "  Initializing database..."
python3 -c "from db.database import init_db; init_db()" 2>/dev/null || true

echo "✅ Backend ready"
echo ""

# Frontend setup
echo "📦 Setting up frontend..."
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "  Installing npm packages..."
    npm install -q
fi

echo "✅ Frontend ready"
echo ""

echo "🚀 Starting CraveLess..."
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Start backend in background
cd ../backend
source venv/bin/activate
python3 main.py > /tmp/craveless_backend.log 2>&1 &
BACKEND_PID=$!

# Start frontend
cd ../frontend
npm run dev

# Cleanup
kill $BACKEND_PID 2>/dev/null
