# How to Run IGotYou Application

This guide will help you set up and run the complete IGotYou application from scratch.

## 📋 Prerequisites

Before starting, make sure you have:

- **Python 3.8+** installed ([download](https://www.python.org/downloads/))
- **Node.js 18+** installed ([download](https://nodejs.org/))
- **Google API Key** for Gemini AI (from [Google AI Studio](https://aistudio.google.com/))
- **Google Maps API Key** (from [Google Cloud Console](https://console.cloud.google.com/))

## 🔧 Step 1: Set Up Environment Variables

1. **Create a `.env` file** in the **root directory** of the project (same level as `backend/`, `frontend/`, and `IGotYou_Agent/`).

2. **Add your API keys** to the `.env` file:

```env
# Google API Key for Gemini AI (required for the agent)
GOOGLE_API_KEY=your_google_api_key_here

# Google Maps API Key (required for Google Maps and Places API)
GOOGLE_MAPS_API=your_google_maps_api_key_here

# Frontend environment variables
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
NEXT_PUBLIC_API_URL=http://localhost:8000

# Optional: CORS origins (comma-separated)
CORS_ORIGINS=http://localhost:3000
```

**Important Notes:**
- Replace `your_google_api_key_here` and `your_google_maps_api_key_here` with your actual API keys
- The `GOOGLE_API_KEY` is used by the backend agent (IGotYou_Agent)
- The `GOOGLE_MAPS_API` is used by the agent for Google Places API calls
- The `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY` is used by the frontend for displaying maps

## 📦 Step 2: Install Dependencies

### Install Backend Dependencies

Open a terminal and navigate to the project root, then:

```bash
cd backend
pip install -r requirements.txt
```

This installs:
- FastAPI (web framework)
- Uvicorn (ASGI server)
- Google ADK (Agent Development Kit)
- Google GenAI SDK
- Google Maps Python client
- Other dependencies

### Install Frontend Dependencies

In a new terminal window (or after finishing backend setup):

```bash
cd frontend
npm install
```

This installs:
- Next.js (React framework)
- React
- TypeScript
- Tailwind CSS
- Google Maps API loader
- Other UI dependencies

## 🚀 Step 3: Run the Application

You need to run **both the backend and frontend** servers. You can use the provided startup scripts or run them manually.

### Option A: Using Startup Scripts (Recommended)

#### Windows:
```bash
start.bat
```

#### Linux/Mac:
```bash
chmod +x start.sh
./start.sh
```

This will automatically start both servers in separate windows/processes.

### Option B: Manual Start (Two Terminal Windows)

#### Terminal 1: Start Backend Server

```bash
cd backend
python main.py
```

You should see:
```
============================================================
🚀 Starting I Got You Backend API Server
============================================================
📍 Server will run at: http://localhost:8000
📚 API Docs available at: http://localhost:8000/docs
🔄 Waiting for requests...
============================================================
```

**Backend is now running at:**
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/

#### Terminal 2: Start Frontend Server

```bash
cd frontend
npm run dev
```

You should see:
```
  ▲ Next.js 16.x
  - Local:        http://localhost:3000
```

**Frontend is now running at:** http://localhost:3000

## ✅ Step 4: Verify Everything Works

1. **Open your browser** and go to: http://localhost:3000

2. **You should see:**
   - Beautiful homepage with "I Got You" branding
   - "Start Discovering" button

3. **Test the application:**
   - Click "Start Discovering"
   - Enter a search query like: "quiet surf spot in Bali for beginners"
   - Click "Discover Hidden Gems"
   - Wait for results (this may take 10-30 seconds)
   - You should see hidden gems with photos, maps, and AI analysis

4. **Check the backend:**
   - Visit http://localhost:8000/docs to see the API documentation
   - Visit http://localhost:8000/ to see the health check

## 🏗️ Architecture Overview

```
IGotYou/
├── backend/              # FastAPI backend server (port 8000)
│   └── main.py          # Connects to IGotYou_Agent and exposes REST API
│
├── frontend/            # Next.js frontend (port 3000)
│   ├── app/            # Next.js app router pages
│   └── components/     # React components
│
└── IGotYou_Agent/       # Python AI agent (used by backend)
    ├── agent.py        # Main agent orchestrator
    ├── config.py       # Configuration and API keys
    └── sub_Agents/     # Specialized sub-agents
        ├── discovery_agent.py      # Finds places using Google Places
        ├── analysis_agent.py       # Filters and analyzes places
        └── recommendation_agent.py # Formats final response
```

## 🔄 How It Works

1. **User enters search query** in the frontend
2. **Frontend sends request** to Next.js API route (`/api/discover`)
3. **Next.js API route** forwards to FastAPI backend (`/api/discover`)
4. **Backend calls IGotYou_Agent** with the query
5. **Agent processes query** through 3 sub-agents:
   - **Discovery Agent**: Searches Google Places API
   - **Analysis Agent**: Filters results (hidden gems criteria)
   - **Recommendation Agent**: Formats beautiful response
6. **Response flows back** through backend → frontend → user

## 🐛 Troubleshooting

### Backend won't start

**Error: "Missing GOOGLE_API_KEY in .env"**
- Check that your `.env` file exists in the root directory
- Verify `GOOGLE_API_KEY` is set correctly

**Error: "Module not found"**
- Make sure you installed backend dependencies: `cd backend && pip install -r requirements.txt`
- Check that you're using Python 3.8+

**Error: "Cannot import IGotYou_Agent"**
- The backend should automatically find the agent (it adds parent directory to path)
- Verify the `IGotYou_Agent/` folder exists in the project root

### Frontend won't start

**Error: "Cannot find module"**
- Make sure you installed frontend dependencies: `cd frontend && npm install`
- Check that Node.js 18+ is installed

**Error: "Backend server not available"**
- Make sure the backend is running on port 8000
- Check that `NEXT_PUBLIC_API_URL` in `.env` is set to `http://localhost:8000`

### Maps not displaying

**Error: "Google Maps not loading"**
- Check that `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY` is set in `.env`
- Verify the API key is valid
- Make sure Maps JavaScript API is enabled in Google Cloud Console

### Agent returns errors

**Error: "API returned ZERO_RESULTS"**
- The query might be too specific
- Try a broader search query

**Error: "Error processing request"**
- Check backend terminal for detailed error messages
- Verify both `GOOGLE_API_KEY` and `GOOGLE_MAPS_API` are set correctly
- Check that your API keys have the necessary permissions enabled

## 🔑 API Keys Setup Guide

### Getting Google API Key (for Gemini)

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Click "Get API Key"
3. Create a new project or select existing
4. Copy the API key
5. Add to `.env` as `GOOGLE_API_KEY`

### Getting Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable the following APIs:
   - **Maps JavaScript API** (for frontend maps)
   - **Places API** (for searching places)
   - **Places API (New)** (if available)
4. Go to "Credentials" → "Create Credentials" → "API Key"
5. Copy the API key
6. Add to `.env` as both `GOOGLE_MAPS_API` and `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY`

**Important:** Set spending limits on your API keys to avoid unexpected charges!

## 📝 Development Commands

### Backend
```bash
cd backend
python main.py                    # Start server
uvicorn main:app --reload        # Start with auto-reload (for development)
```

### Frontend
```bash
cd frontend
npm run dev          # Start development server
npm run build        # Build for production
npm start            # Start production server
npm run lint         # Run ESLint
```

## 🛑 Stopping the Servers

- **If using startup scripts**: Close the terminal windows or press Ctrl+C
- **If running manually**: Press Ctrl+C in each terminal window

## 📚 Additional Resources

- **API Documentation**: http://localhost:8000/docs (when backend is running)
- **SETUP_GUIDE.md**: More detailed setup instructions
- **README.md**: General project information

## ✅ Quick Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js 18+ installed
- [ ] `.env` file created in root directory
- [ ] `GOOGLE_API_KEY` added to `.env`
- [ ] `GOOGLE_MAPS_API` added to `.env`
- [ ] `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY` added to `.env`
- [ ] Backend dependencies installed (`pip install -r backend/requirements.txt`)
- [ ] Frontend dependencies installed (`npm install` in `frontend/` directory)
- [ ] Backend server running (http://localhost:8000)
- [ ] Frontend server running (http://localhost:3000)
- [ ] Application works in browser

---

**Need help?** Check the error messages in your terminal or browser console for detailed information about what went wrong.


