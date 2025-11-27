# 🚀 Quick Start Guide

## Three Ways to Start I Got You

### Option 1: One-Command Startup (Recommended) 🎯

**Mac/Linux:**
```bash
./start.sh
```

**Windows:**
```bash
start.bat
```

This will:
- ✅ Check prerequisites (Python, Node.js)
- ✅ Start both backend and frontend automatically
- ✅ Show status of both servers
- ✅ Stop both servers with Ctrl+C (Mac/Linux)

---

### Option 2: Start with Visual Feedback 📊

The frontend has a **built-in backend status indicator** that will:
- 🟡 Show a warning banner when backend is offline
- 📋 Display copy-paste commands to start the backend
- 🔄 Auto-recheck backend status every 10 seconds
- ✅ Automatically hide when backend is online

**Step 1:** Start the frontend
```bash
cd frontend
npm run dev
```

**Step 2:** Visit http://localhost:3000/discover
- You'll see a yellow banner with instructions
- Click "Show Instructions" for detailed help
- Click "Copy" to copy the backend start command

**Step 3:** Start the backend as instructed
```bash
cd backend
python main.py
```

The banner will disappear automatically when the backend is online!

---

### Option 3: Manual Start (Two Terminals) 🖥️

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

Wait for:
```
🚀 Starting I Got You Backend API Server
📍 Server will run at: http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Wait for:
```
▲ Next.js 16.x
- Local:        http://localhost:3000
```

---

## 🎉 You're Ready!

Once both servers are running:

1. **Open your browser:** http://localhost:3000
2. **Click "Start Discovering"**
3. **Try a search:**
   - "quiet surf spot in Bali for beginners"
   - "hidden beach in Mexico for snorkeling"
   - "lesser-known hiking trail near Vancouver"

## 🐛 Troubleshooting

### Backend Not Running?
The UI will show a yellow banner with instructions. Click "Show Instructions" for help.

### Still Having Issues?
Check the detailed [SETUP_GUIDE.md](SETUP_GUIDE.md)

---

## 📊 Monitoring

### Logs to Watch:

**Browser Console (F12):**
```
[Frontend] Starting search with query: ...
[Frontend] Response status: 200
```

**Frontend Terminal:**
```
[Next.js API] Received search query: ...
[Next.js API] Backend response status: 200
```

**Backend Terminal:**
```
[Backend] Received search query: ...
[Backend] Successfully parsed 2 gems
[Backend] Processing time: 15.32s
```

---

## 🛑 Stopping the Servers

**If using start.sh (Mac/Linux):**
- Press `Ctrl+C` in the terminal

**If using start.bat (Windows):**
- Close the terminal windows

**If running manually:**
- Press `Ctrl+C` in each terminal

---

## ⚡ Pro Tips

1. **First time setup?** Read [SETUP_GUIDE.md](SETUP_GUIDE.md) for environment variables
2. **API not working?** Check that your `.env` file has valid API keys
3. **Want API docs?** Visit http://localhost:8000/docs when backend is running
4. **Google Maps not loading?** Verify `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY` in `.env`

---

Happy discovering! 🌴🏖️
