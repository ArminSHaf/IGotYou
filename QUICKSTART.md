# Quick Start Guide

Get I Got You running in 3 steps.

## Prerequisites

- Python 3.13+ and Node.js 18+
- Google API keys in `.env` file (see `.env.example`)

## Option 1: One-Command Start

Mac/Linux:
```bash
./start.sh
```

Windows:
```bash
start.bat
```

## Option 2: Manual Start (Two Terminals)

Terminal 1 - Backend:
```bash
cd backend
python main.py
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

## You're Ready

1. Open http://localhost:3000
2. Click "Start Discovering"
3. Try: "quiet surf spot in Bali for beginners"

## Access Points

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

## Quick Fixes

Backend won't start?
```bash
pip install -r requirements.txt
```

Frontend won't start?
```bash
cd frontend && npm install
```

API key errors? Check `.env` has valid keys.

## Test the Agent

```bash
python test_agent.py
```

For detailed setup, see [SETUP_GUIDE.md](SETUP_GUIDE.md)
