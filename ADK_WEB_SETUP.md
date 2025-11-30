# ADK Web Interface Setup for IGotYou Agent

This guide shows you how to use Google's built-in ADK web interface to chat with your IGotYou agent.

## 🎯 What is ADK Web?

ADK (Agent Development Kit) provides a built-in web chat UI that automatically works with any ADK agent. Instead of building a custom frontend, you can use this interface to interact with your agent through a clean chat interface.

## ✅ Prerequisites

1. **Virtual environment activated** with all dependencies installed:
   ```bash
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate.bat  # On Windows
   ```

2. **Environment variables configured** in `.env` file:
   - `GOOGLE_API_KEY` - Your Google AI API key (required)
   - `GOOGLE_MAPS_API` - Your Google Maps API key (required)
   - `ACCUWEATHER_API_KEY` - AccuWeather API key (optional, for weather features)

## 🚀 Quick Start

### Option 1: Use the startup script (Recommended)

**On macOS/Linux:**
```bash
./start_adk_web.sh
```

**On Windows:**
```bash
start_adk_web.bat
```

### Option 2: Run the command directly

```bash
adk web IGotYou/agent.py
```

## 🌐 Accessing the Interface

Once the server starts, open your browser and go to:

```
http://localhost:8000
```

You'll see a chat interface where you can interact with your IGotYou agent!

## 💬 How to Use

1. **Start a conversation**: Type your request in the chat box
   - Example: "Find me a hidden gem in Munich"

2. **Answer clarifying questions**: The agent will ask follow-up questions to understand:
   - What TYPE of experience you want (adventure, relaxation, photography, etc.)
   - WHO you're going with (solo, couple, family, friends)
   - Any timing preferences or constraints

3. **Get recommendations**: The agent will find 3 hidden gems that match your preferences

4. **Select a location**: Choose which gem you want to visit

5. **Get weather & outfit advice**: The agent will check real-time weather (via MCP) and give you personalized recommendations

## 🔧 How It Works

The `adk web` command:
- Reads your `IGotYou/agent.py` file
- Looks for the exported `root_agent` and `runner`
- Automatically generates a web UI
- Starts a local server at http://localhost:8000
- Provides a chat interface to interact with your agent

## 🎨 Agent Capabilities

Your IGotYou agent has:

✅ **Intent Understanding Loop** - Asks clarifying questions to understand your needs
✅ **Hidden Gem Discovery** - Searches Google Places for lesser-known spots
✅ **Analysis Agent** - Filters by "hidden gem" criteria (low reviews, high ratings)
✅ **Recommendation Agent** - Generates AI insights from reviews
✅ **Weather MCP Integration** - Real-time weather data via Model Context Protocol
✅ **Google Images Tool** - Fetches scenic images for each location

## 🛠️ Troubleshooting

### Server won't start

**Check dependencies:**
```bash
pip install -r requirements.txt
```

**Verify environment variables:**
```bash
cat .env  # Should show GOOGLE_API_KEY and GOOGLE_MAPS_API
```

### Agent errors during conversation

**Check the terminal output** - The ADK web interface shows detailed logs in the terminal where you started the server. Look for error messages there.

**Common issues:**
- Missing API keys → Add them to `.env`
- Rate limits → Wait a moment and try again
- MCP weather server not found → Weather features will be disabled, but the agent still works

### Port already in use

If port 8000 is already taken, you can specify a different port:
```bash
adk web IGotYou/agent.py --port 8080
```

Then access at: http://localhost:8080

## 📝 Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

## 🔄 Comparison: ADK Web vs Custom Frontend

| Feature | ADK Web | Custom Next.js Frontend |
|---------|---------|-------------------------|
| Setup Time | ⚡ Instant | 🕐 Requires development |
| Chat Interface | ✅ Built-in | ❌ Need to build |
| Agent Integration | ✅ Automatic | ⚙️ Manual API setup |
| Customization | ❌ Limited | ✅ Full control |
| UI Design | 📱 Google's default | 🎨 Custom white theme |
| Best For | Testing & demos | Production apps |

## 🎯 Next Steps

Once your agent works well with ADK web, you can:
1. Keep using ADK web for demos and testing
2. Build a custom frontend when you need specific UI/UX
3. Deploy the ADK web interface to production if it meets your needs

## 📚 Additional Resources

- [Google ADK Documentation](https://cloud.google.com/generative-ai-app-builder/docs/agent-development-kit)
- [Agent Development Kit GitHub](https://github.com/google/agent-development-kit)
- [MCP Protocol Documentation](https://modelcontextprotocol.io/)

---

**Ready to chat with your agent?** Run `./start_adk_web.sh` and open http://localhost:8000! 🚀
