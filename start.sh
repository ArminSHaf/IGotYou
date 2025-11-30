#!/bin/bash

# I Got You - Startup Script
# This script starts both the frontend and backend servers

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           🚀 Starting I Got You Application                  ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Warning: .env file not found!${NC}"
    echo "Please create a .env file with your API keys."
    echo "See SETUP_GUIDE.md for details."
    echo ""
    exit 1
fi

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command_exists python3; then
    echo -e "${YELLOW}❌ Python 3 is not installed${NC}"
    exit 1
fi

if ! command_exists node; then
    echo -e "${YELLOW}❌ Node.js is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ All prerequisites met${NC}"
echo ""

# Create a temporary file to store PIDs
PIDFILE="./.running_servers.pid"
rm -f "$PIDFILE"

# Cleanup function
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    if [ -f "$PIDFILE" ]; then
        while read pid; do
            if ps -p $pid > /dev/null 2>&1; then
                kill $pid 2>/dev/null
            fi
        done < "$PIDFILE"
        rm -f "$PIDFILE"
    fi
    echo "✓ All servers stopped"
    exit 0
}

# Set up trap to catch Ctrl+C
trap cleanup INT TERM

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}📦 Starting Backend Server (Python/FastAPI)...${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start backend in background
cd backend
python3 main.py &
BACKEND_PID=$!
echo $BACKEND_PID >> "../$PIDFILE"
cd ..

# Wait a bit for backend to start
sleep 3

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}🎨 Starting Frontend Server (Next.js)...${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start frontend in background
cd frontend
npm run dev &
FRONTEND_PID=$!
echo $FRONTEND_PID >> "../$PIDFILE"
cd ..

# Wait a bit for frontend to start
sleep 5

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    ✅ Servers Running!                       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}🌐 Frontend:${NC}  http://localhost:3000"
echo -e "${GREEN}🔧 Backend:${NC}   http://localhost:8000"
echo -e "${GREEN}📚 API Docs:${NC}  http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Wait for user to stop the servers
wait
