# 🚀 IGotYou Agent - Quick Start Guide

## What You Have Now

Your IGotYou agent is ready to use with **two different interfaces**:

1. **ADK Web Interface** ⭐ **RECOMMENDED** - Google's built-in chat UI (fastest way to test)
2. **Custom Next.js Frontend** - Your white-themed web app (for production)

---

## ⚡ Quick Start (ADK Web - Recommended)

### 1. Activate Virtual Environment

```bash
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate.bat  # Windows
```

### 2. Start ADK Web Interface

```bash
./start_adk_web.sh  # macOS/Linux
# or
start_adk_web.bat   # Windows
```

### 3. Open Browser

Navigate to: **http://localhost:8000**

### 4. Chat with Your Agent!

Try asking:
- "Find me a hidden gem in Munich"
- "I want a quiet beach in Bali"
- "Hidden hiking trails near Zurich"

The agent will:
1. Ask clarifying questions to understand your needs
2. Search for hidden gems using Google Places
3. Analyze reviews with AI
4. Check real-time weather (via MCP)
5. Give personalized recommendations

---

## 🎨 Alternative: Custom Frontend

If you prefer the custom Next.js UI:

### Terminal 1 - Backend
```bash
cd backend
python main.py
```

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

Open: **http://localhost:3000**

---

## 📋 Prerequisites Checklist

✅ Virtual environment activated (`source venv/bin/activate`)
✅ Dependencies installed (`pip install -r requirements.txt`)
✅ Environment variables in `.env` file:
   - `GOOGLE_API_KEY` - Your Google AI API key
   - `GOOGLE_MAPS_API` - Your Google Maps API key
   - `ACCUWEATHER_API_KEY` - (Optional) For weather features

---

## 🎯 Which Interface Should I Use?

| Feature | ADK Web | Custom Frontend |
|---------|---------|-----------------|
| **Setup** | ⚡ 1 command | 🔧 2 terminals |
| **Best For** | Testing, demos, development | Production, custom UX |
| **UI** | Google's default chat | Your white theme |
| **Agent Features** | ✅ All features work | ✅ All features work |
| **Customization** | ❌ Limited | ✅ Full control |

**Recommendation**: Start with **ADK Web** for testing. It's faster and easier to use!

---

## 🛠️ Troubleshooting

### ADK Web won't start

1. **Check virtual environment is activated**:
   ```bash
   which python3  # Should show path inside venv/
   ```

2. **Verify dependencies**:
   ```bash
   pip install google-adk
   ```

3. **Check environment variables**:
   ```bash
   cat .env  # Should show your API keys
   ```

### Agent errors during conversation

- **Check terminal output** - Detailed error logs appear in the terminal
- **Missing API key** - Make sure `.env` has `GOOGLE_API_KEY` and `GOOGLE_MAPS_API`
- **Rate limit** - Wait a moment and try again

### Port 8000 already in use

Run on a different port:
```bash
adk web IGotYou/agent.py --port 8080
```

---

## 📚 Additional Documentation

- **[ADK_WEB_SETUP.md](ADK_WEB_SETUP.md)** - Complete ADK Web guide
- **[readme.md](readme.md)** - Full project documentation
- **Backend API**: Run backend then visit http://localhost:8000/docs

---

## 🎉 You're Ready!

Run this now:
```bash
./start_adk_web.sh
```

Then open **http://localhost:8000** and start discovering hidden gems! 🗺️✨
