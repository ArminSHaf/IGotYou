# I Got You - Setup Guide

Complete setup instructions for the IGotYou application.

## Project Structure

```
IGotYou/
├── .env                    # Environment variables (single source)
├── .env.example            # Template
├── requirements.txt        # Python dependencies
│
├── agent/                  # AI Agent Package
│   ├── __init__.py
│   ├── agent.py            # Main orchestrator
│   ├── config.py           # Configuration
│   └── sub_agents/
│       ├── discovery_agent.py
│       ├── analysis_agent.py
│       └── recommendation_agent.py
│
├── backend/                # FastAPI Backend
│   └── main.py
│
├── frontend/               # Next.js Frontend
│   ├── .env -> ../.env     # Symlink to root
│   └── ...
│
├── test_agent.py           # Agent test script
├── start.sh                # Mac/Linux startup
└── start.bat               # Windows startup
```

## Prerequisites

- Node.js 18+
- Python 3.13+
- Google API Key (from https://aistudio.google.com/)
- Google Maps API Key (from https://console.cloud.google.com/)

## Step 1: Environment Variables

Copy the example file:
```bash
cp .env.example .env
```

Edit `.env` and add your keys:
```env
GOOGLE_API_KEY=your_google_api_key_here
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
NEXT_PUBLIC_API_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:3000
```

Note: `frontend/.env` is a symlink to the root `.env` file.

## Step 2: Install Dependencies

Python:
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Frontend:
```bash
cd frontend
npm install
```

## Step 3: Run

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

Open http://localhost:3000

## Troubleshooting

### Module not found
```bash
pip install -r requirements.txt
```

### Frontend can't connect to backend
1. Check backend is running on port 8000
2. Verify NEXT_PUBLIC_API_URL in .env

### Google Maps not displaying
1. Check NEXT_PUBLIC_GOOGLE_MAPS_API_KEY
2. Enable Maps JavaScript API in Google Cloud Console

### Agent returns 403 PERMISSION_DENIED
1. Go to https://console.cloud.google.com/apis/library
2. Enable 'Generative Language API'

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| / | GET | Health check |
| /api/discover | POST | Main discovery endpoint |
| /docs | GET | Swagger documentation |

## Deployment

Backend (Railway / Fly.io):
1. Connect GitHub repo
2. Set GOOGLE_API_KEY and CORS_ORIGINS
3. Deploy

Frontend (Vercel):
1. Import to Vercel
2. Set environment variables
3. Deploy
