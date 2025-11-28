# MCP Weather Integration Guide for IGotYou Agent

## Overview

This guide walks you through integrating the MCP weather server (https://github.com/adhikasp/mcp-weather) into your IGotYou agent to provide weather data and clothing recommendations for discovered hidden gems.

**Important**: This is a **guide only** - you'll modify all code yourself. I'm here to answer questions and provide clarification as you implement.

---

## Architecture Summary

### Current Flow
```
User Query → FastAPI → Root Agent (Sequential)
  ├─ Discovery Agent (Google Places search)
  ├─ Analysis Agent (Filter & fetch reviews)
  └─ Recommendation Agent (Generate insights)
```

### Enhanced Flow with MCP Weather
```
User Query → FastAPI → Root Agent (Sequential)
  ├─ Discovery Agent (Google Places search)
  ├─ Analysis Agent (Filter & fetch reviews)
  ├─ Recommendation Agent (Generate insights)
  └─ Weather Agent (MCP weather + clothing advice) ← NEW
```

---

## Phase 1: MCP Weather Server Setup

### 1.1 Get AccuWeather API Key

1. Go to https://developer.accuweather.com/
2. Create a free account
3. Get your API key (limited to 50 calls/day on free tier)
4. Save the key - you'll need it for environment configuration

### 1.2 Install MCP Weather Server

The MCP weather server is a Python package that needs to be installed in your system:

```bash
# Option A: Install from GitHub directly
cd /tmp
git clone https://github.com/adhikasp/mcp-weather.git
cd mcp-weather
uv venv
uv sync

# Option B: Use npx/uvx for running (if available)
# This runs it directly without cloning
```

**Testing the server independently:**
```bash
# Set your API key
export ACCUWEATHER_API_KEY="your_key_here"

# Run the server to verify it works
# (Exact command depends on the mcp-weather package structure)
uvx mcp-weather
```

### 1.3 Update Environment Configuration

Add to your `.env` file:

```env
# Existing keys...
GOOGLE_API_KEY=...
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=...
NEXT_PUBLIC_API_URL=http://localhost:8000

# NEW: AccuWeather API key for MCP weather server
ACCUWEATHER_API_KEY=your_accuweather_key_here
```

---

## Phase 2: Python MCP Client Integration

### 2.1 Understanding MCP Architecture

**MCP Components:**
- **MCP Server** (Node.js/Python): Runs as separate process, exposes weather tools
- **Transport Layer**: stdio (standard input/output) or SSE (server-sent events)
- **MCP Client** (Python): Your agent uses this to call MCP server tools
- **ClientSession**: Manages connection and tool invocation

**Key imports available:**
```python
from mcp import (
    ClientSession,
    StdioServerParameters,
    stdio_client
)
```

### 2.2 Create MCP Weather Tool Wrapper

**Create new file**: `/IGotYou_Agent/mcp_tools/weather_tool.py`

This file will:
1. Start the MCP weather server as subprocess
2. Connect via stdio transport
3. Provide a function to call weather tools
4. Handle errors gracefully

**Pseudocode structure:**
```python
import asyncio
from mcp import ClientSession, StdioServerParameters, stdio_client
import os

# Configuration for the MCP weather server
def get_weather_server_params():
    """Returns StdioServerParameters for the MCP weather server"""
    return StdioServerParameters(
        command="uvx",  # or full path to the mcp-weather executable
        args=["mcp-weather"],  # adjust based on actual package
        env={
            "ACCUWEATHER_API_KEY": os.getenv("ACCUWEATHER_API_KEY")
        }
    )

async def get_weather_for_location(latitude: float, longitude: float) -> dict:
    """
    Calls MCP weather server to get weather forecast for coordinates.

    Returns:
        dict with weather data including:
        - location: {name, key, country}
        - current: {temperature, description, humidity, hasPrecipitation}
        - forecast: list of hourly forecasts (12 hours)
    """
    server_params = get_weather_server_params()

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()

            # List available tools
            tools = await session.list_tools()

            # Find the weather tool (name might be "get_weather" or similar)
            # Check tools.tools array for the actual tool name

            # Call the weather tool
            result = await session.call_tool(
                name="get_weather",  # Adjust based on actual tool name
                arguments={
                    "latitude": latitude,
                    "longitude": longitude
                }
            )

            return result.content

def weather_tool_sync(latitude: float, longitude: float) -> dict:
    """
    Synchronous wrapper for the async weather function.
    Google ADK tools need synchronous functions.
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(
        get_weather_for_location(latitude, longitude)
    )
```

**Key considerations:**
- The actual tool name from MCP server might be different (check MCP weather docs)
- You may need to adjust the command/args for your system
- Error handling: What if MCP server is down? Return fallback data

---

## Phase 3: Create Weather Agent

### 3.1 New Agent File

**Create**: `/IGotYou_Agent/sub_Agents/weather_agent.py`

This agent will:
1. Receive gem data from Recommendation Agent (with coordinates)
2. Call MCP weather tool for each gem's coordinates
3. Use Gemini to generate clothing recommendations based on weather
4. Return enriched data with weather + clothing fields

**Structure:**
```python
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types
from ..mcp_tools.weather_tool import weather_tool_sync

# Retry configuration
retry_config = types.HttpRetryOptions(
    attempts=3,
    exp_base=2,
    initial_delay=1,
    http_status_codes=[429, 500, 503]
)

def get_weather_and_clothing_tool(gems_data: list[dict]) -> dict:
    """
    For each gem, fetches weather and generates clothing recommendations.

    Input: gems_data from Recommendation Agent
    Output: Same gems with added weather and clothing fields
    """
    enriched_gems = []

    for gem in gems_data:
        try:
            # Extract coordinates
            coords = gem.get("coordinates", {})
            lat = coords.get("lat")
            lng = coords.get("lng")

            if not lat or not lng:
                # Skip if no coordinates
                enriched_gems.append(gem)
                continue

            # Call MCP weather server
            weather_data = weather_tool_sync(lat, lng)

            # Add weather info to gem
            gem["weather"] = {
                "temperature": weather_data.get("current", {}).get("temperature"),
                "conditions": weather_data.get("current", {}).get("description"),
                "humidity": weather_data.get("current", {}).get("humidity"),
                "hasPrecipitation": weather_data.get("current", {}).get("hasPrecipitation")
            }

            enriched_gems.append(gem)

        except Exception as e:
            print(f"Error fetching weather for {gem.get('placeName')}: {e}")
            # Add fallback weather data
            gem["weather"] = {
                "temperature": None,
                "conditions": "Weather unavailable",
                "humidity": None,
                "hasPrecipitation": False
            }
            enriched_gems.append(gem)

    return {"gems": enriched_gems}

# Define the Weather Agent
weather_agent = Agent(
    name="Weather_Agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="Enriches gems with weather data and clothing recommendations",
    instruction="""
    You are the **Weather Agent**.

    You will receive a list of hidden gems with weather data already fetched.

    YOUR JOB:
    1. For EACH gem, analyze the weather conditions (temperature, conditions, precipitation, humidity)
    2. Generate practical clothing recommendations based on:
       - Temperature (hot, warm, cool, cold)
       - Conditions (sunny, cloudy, rainy, etc.)
       - Precipitation status
       - Type of outdoor activity (hiking, beach, etc.)

    3. Add a "clothingRecommendation" field to each gem's analysis section with 1-2 sentences

    Example clothing recommendations:
    - "Bring light, breathable clothing and plenty of sunscreen. A wide-brimmed hat is essential."
    - "Layer up with a warm jacket and waterproof outer shell. Waterproof hiking boots recommended."
    - "Pack a rain jacket and quick-dry clothing. The trail can get muddy after rain."

    4. Return the complete gems array with the added clothingRecommendation field

    CRITICAL: Return the COMPLETE JSON structure with all existing fields plus the new clothingRecommendation
    """,
    tools=[get_weather_and_clothing_tool]
)
```

### 3.2 Integrate Weather Agent into Root Agent

**Edit**: `/IGotYou_Agent/agent.py`

```python
# Add import
from .sub_Agents import (
    analysis_agent,
    discovery_agent,
    recommendation_agent,
    weather_agent,  # NEW
)

# Update root agent
root_agent = SequentialAgent(
    name="IGOTYOU_Agent",
    description="Your role is to manage user interaction and delegate to specialized sub-agents to find hidden outdoor gems",
    sub_agents=[
        discovery_agent,      # Phase 1: Find candidates
        analysis_agent,       # Phase 2: Filter & analyze
        recommendation_agent, # Phase 3: Generate insights
        weather_agent,        # Phase 4: Add weather + clothing ← NEW
    ],
)
```

### 3.3 Update Sub-Agents Module

**Edit**: `/IGotYou_Agent/sub_Agents/__init__.py`

```python
from .discovery_agent import discovery_agent
from .analysis_agent import analysis_agent
from .Recommendation_agent import recommendation_agent
from .weather_agent import weather_agent  # NEW

__all__ = [
    "discovery_agent",
    "analysis_agent",
    "recommendation_agent",
    "weather_agent",  # NEW
]
```

---

## Phase 4: Update Data Schemas

### 4.1 Backend Pydantic Models

**Edit**: `/backend/main.py`

Add new fields to existing models:

```python
# Add Weather model
class Weather(BaseModel):
    temperature: Optional[float] = None
    conditions: Optional[str] = None
    humidity: Optional[int] = None
    hasPrecipitation: bool = False

# Update Analysis model
class Analysis(BaseModel):
    whySpecial: str
    bestTime: str
    insiderTip: str
    clothingRecommendation: Optional[str] = None  # NEW

# Update HiddenGem model
class HiddenGem(BaseModel):
    placeName: str
    address: str
    coordinates: Coordinates
    rating: float
    reviewCount: int
    photos: List[str]
    analysis: Analysis
    weather: Optional[Weather] = None  # NEW
```

### 4.2 Frontend TypeScript Interfaces

**Edit**: `/frontend/types/index.ts`

```typescript
// Add Weather interface
export interface Weather {
  temperature: number | null;
  conditions: string;
  humidity: number | null;
  hasPrecipitation: boolean;
}

// Update Analysis interface
export interface Analysis {
  whySpecial: string;
  bestTime: string;
  insiderTip: string;
  clothingRecommendation?: string; // NEW
}

// Update HiddenGem interface
export interface HiddenGem {
  placeName: string;
  address: string;
  coordinates: Coordinates;
  rating: number;
  reviewCount: number;
  photos: string[];
  analysis: Analysis;
  weather?: Weather; // NEW
}
```

---

## Phase 5: Frontend UI Changes

### 5.1 Update ResultCard Component

**Edit**: `/frontend/components/results/ResultCard.tsx`

Add weather display section after the analysis section:

```typescript
// Inside the ResultCard component, after the analysis section:

{/* Weather & Clothing Section */}
{gem.weather && (
  <div className="space-y-3">
    <h3 className="font-semibold text-lg">Weather & What to Bring</h3>

    {/* Weather Info */}
    <div className="flex items-center gap-4 p-4 bg-blue-50 rounded-lg">
      <div className="flex items-center gap-2">
        {gem.weather.temperature !== null && (
          <>
            <span className="text-2xl">🌡️</span>
            <span className="font-medium">{Math.round(gem.weather.temperature)}°F</span>
          </>
        )}
      </div>
      <div className="flex items-center gap-2">
        <span className="text-2xl">
          {gem.weather.hasPrecipitation ? '🌧️' : '☀️'}
        </span>
        <span>{gem.weather.conditions}</span>
      </div>
      {gem.weather.humidity !== null && (
        <div className="flex items-center gap-2">
          <span className="text-2xl">💧</span>
          <span>{gem.weather.humidity}%</span>
        </div>
      )}
    </div>

    {/* Clothing Recommendation */}
    {gem.analysis.clothingRecommendation && (
      <div className="p-4 bg-amber-50 rounded-lg border-l-4 border-amber-500">
        <div className="flex gap-3">
          <span className="text-2xl">👕</span>
          <div>
            <h4 className="font-medium text-amber-900 mb-1">What to Wear</h4>
            <p className="text-amber-800">{gem.analysis.clothingRecommendation}</p>
          </div>
        </div>
      </div>
    )}
  </div>
)}
```

**Icon suggestions:**
- Temperature: 🌡️
- Sunny: ☀️
- Rainy: 🌧️
- Cloudy: ☁️
- Humidity: 💧
- Clothing: 👕 or 🎽

---

## Phase 6: Error Handling & Fallbacks

### 6.1 MCP Server Connection Failures

Handle cases where MCP server is unavailable:

**In weather_tool.py:**
```python
def weather_tool_sync(latitude: float, longitude: float) -> dict:
    try:
        # ... MCP connection code ...
    except Exception as e:
        print(f"❌ MCP Weather Server Error: {e}")
        # Return fallback data
        return {
            "current": {
                "temperature": None,
                "description": "Weather data unavailable",
                "humidity": None,
                "hasPrecipitation": False
            }
        }
```

### 6.2 Backend Health Check

**Add MCP health check endpoint** in `/backend/main.py`:

```python
@app.get("/health/mcp")
async def mcp_health_check():
    """Check if MCP weather server is accessible"""
    try:
        # Attempt to connect to MCP server
        # (You'll implement this based on your MCP setup)
        return {"status": "healthy", "mcp_weather": "available"}
    except Exception as e:
        return {"status": "degraded", "mcp_weather": "unavailable", "error": str(e)}
```

### 6.3 Frontend Graceful Degradation

If weather data is missing, the UI should still work:

```typescript
// In ResultCard.tsx - only show weather section if data exists
{gem.weather && gem.weather.conditions !== "Weather data unavailable" && (
  // ... weather display ...
)}
```

---

## Phase 7: Testing Strategy

### 7.1 Test MCP Server Independently

Before integrating, verify the MCP server works:

```bash
# Set API key
export ACCUWEATHER_API_KEY="your_key"

# Test with a Python script
python test_mcp_weather.py
```

**test_mcp_weather.py:**
```python
import asyncio
from IGotYou_Agent.mcp_tools.weather_tool import get_weather_for_location

async def test():
    # Test coordinates (San Francisco)
    result = await get_weather_for_location(37.7749, -122.4194)
    print("Weather data:", result)

if __name__ == "__main__":
    asyncio.run(test())
```

### 7.2 Test Weather Agent Isolation

Test the weather agent separately:

```python
# In agent.py or a test script
async def test_weather_agent():
    from IGotYou_Agent.sub_Agents.weather_agent import weather_agent

    mock_gems = {
        "gems": [{
            "placeName": "Test Beach",
            "coordinates": {"lat": 37.7749, "lng": -122.4194},
            "analysis": {
                "whySpecial": "Test",
                "bestTime": "Test",
                "insiderTip": "Test"
            }
        }]
    }

    # Call weather agent
    result = await weather_agent.process(mock_gems)
    print("Enriched data:", result)
```

### 7.3 End-to-End Test

1. Start backend: `python backend/main.py`
2. Start frontend: `cd frontend && npm run dev`
3. Search for a gem: "quiet beach in California"
4. Verify:
   - Weather data appears in response
   - Clothing recommendations are generated
   - UI displays weather section
   - Fallback works if MCP is down

---

## Phase 8: Deployment Considerations

### 8.1 Environment Variables Checklist

Ensure all required variables are set in production:

```env
GOOGLE_API_KEY=...
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=...
NEXT_PUBLIC_API_URL=...
ACCUWEATHER_API_KEY=...  # NEW
```

### 8.2 MCP Server Process Management

**Option A: Run as separate service**
```bash
# Start MCP weather server
uvx mcp-weather &

# Start FastAPI backend
python backend/main.py
```

**Option B: Supervisor/Process Manager**
Use a process manager to ensure MCP server stays running:

```ini
# supervisor.conf
[program:mcp-weather]
command=uvx mcp-weather
environment=ACCUWEATHER_API_KEY="your_key"
autostart=true
autorestart=true

[program:fastapi-backend]
command=python backend/main.py
directory=/path/to/IGotYou
autostart=true
autorestart=true
```

### 8.3 Startup Script

Create a startup script that launches both services:

**start-with-weather.sh:**
```bash
#!/bin/bash
export ACCUWEATHER_API_KEY="your_key"

# Start MCP weather server in background
echo "Starting MCP Weather Server..."
uvx mcp-weather &
MCP_PID=$!

# Wait a moment for MCP server to initialize
sleep 2

# Start FastAPI backend
echo "Starting FastAPI Backend..."
cd backend
python main.py

# Cleanup on exit
trap "kill $MCP_PID" EXIT
```

---

## Phase 9: Optimization & Caching

### 9.1 Cache Weather Data

Weather doesn't change every second - cache it to reduce API calls:

```python
from functools import lru_cache
import time

# Simple in-memory cache with TTL
weather_cache = {}

def get_cached_weather(lat: float, lng: float, ttl_seconds=3600):
    """
    Cache weather data for 1 hour (3600 seconds).
    Reduces AccuWeather API calls.
    """
    cache_key = f"{lat:.4f},{lng:.4f}"
    now = time.time()

    if cache_key in weather_cache:
        cached_data, timestamp = weather_cache[cache_key]
        if now - timestamp < ttl_seconds:
            print(f"✅ Using cached weather for {cache_key}")
            return cached_data

    # Fetch fresh data
    weather_data = weather_tool_sync(lat, lng)
    weather_cache[cache_key] = (weather_data, now)

    return weather_data
```

### 9.2 Parallel Weather Fetching

If fetching weather for 3 gems sequentially is slow, parallelize:

```python
import asyncio

async def get_weather_for_all_gems(gems_data: list[dict]) -> list[dict]:
    """Fetch weather for all gems in parallel"""
    tasks = []
    for gem in gems_data:
        coords = gem.get("coordinates", {})
        task = get_weather_for_location(coords["lat"], coords["lng"])
        tasks.append(task)

    weather_results = await asyncio.gather(*tasks, return_exceptions=True)

    # Combine results with gems
    for i, gem in enumerate(gems_data):
        gem["weather"] = weather_results[i]

    return gems_data
```

---

## Implementation Checklist

Use this as your implementation guide:

- [ ] **Phase 1: MCP Setup**
  - [ ] Get AccuWeather API key
  - [ ] Install MCP weather server
  - [ ] Test MCP server independently
  - [ ] Add ACCUWEATHER_API_KEY to .env

- [ ] **Phase 2: MCP Client**
  - [ ] Create `/IGotYou_Agent/mcp_tools/weather_tool.py`
  - [ ] Implement async MCP connection
  - [ ] Test MCP tool wrapper
  - [ ] Add error handling

- [ ] **Phase 3: Weather Agent**
  - [ ] Create `/IGotYou_Agent/sub_Agents/weather_agent.py`
  - [ ] Implement weather + clothing tool
  - [ ] Update agent imports in `__init__.py`
  - [ ] Add weather_agent to root_agent sequence

- [ ] **Phase 4: Data Schemas**
  - [ ] Update Pydantic models in `/backend/main.py`
  - [ ] Update TypeScript interfaces in `/frontend/types/index.ts`
  - [ ] Test backend response parsing

- [ ] **Phase 5: Frontend UI**
  - [ ] Update ResultCard component
  - [ ] Add weather display section
  - [ ] Add clothing recommendation section
  - [ ] Style with Tailwind CSS

- [ ] **Phase 6: Error Handling**
  - [ ] Add MCP connection fallbacks
  - [ ] Add health check endpoint
  - [ ] Test graceful degradation

- [ ] **Phase 7: Testing**
  - [ ] Test MCP server standalone
  - [ ] Test weather agent isolation
  - [ ] End-to-end integration test

- [ ] **Phase 8: Deployment**
  - [ ] Update environment variables
  - [ ] Create startup script
  - [ ] Test in production-like environment

- [ ] **Phase 9: Optimization** (Optional)
  - [ ] Add weather caching
  - [ ] Parallelize weather fetching

---

## Critical Files to Modify

Here's your complete file modification list:

### New Files to Create
1. `/IGotYou_Agent/mcp_tools/` (new directory)
2. `/IGotYou_Agent/mcp_tools/__init__.py`
3. `/IGotYou_Agent/mcp_tools/weather_tool.py`
4. `/IGotYou_Agent/sub_Agents/weather_agent.py`

### Existing Files to Modify
1. `/IGotYou_Agent/agent.py` - Add weather_agent to sequence
2. `/IGotYou_Agent/sub_Agents/__init__.py` - Export weather_agent
3. `/backend/main.py` - Update Pydantic models (Weather, Analysis, HiddenGem)
4. `/frontend/types/index.ts` - Update TypeScript interfaces
5. `/frontend/components/results/ResultCard.tsx` - Add weather UI section
6. `/.env` - Add ACCUWEATHER_API_KEY

---

## Troubleshooting Guide

### Issue: MCP server won't start
**Solution**:
- Check if `uvx` or `uv` is installed
- Verify ACCUWEATHER_API_KEY is set
- Check mcp-weather package installation

### Issue: "Tool not found" error
**Solution**:
- List available tools: `await session.list_tools()`
- Check the actual tool name from MCP server
- Update tool name in weather_tool.py

### Issue: Agent timeout
**Solution**:
- Increase retry attempts in retry_config
- Add timeout parameter to MCP client
- Cache weather data to reduce calls

### Issue: Weather data not appearing in UI
**Solution**:
- Check browser console for TypeScript errors
- Verify backend response includes weather field
- Check if weather agent is in root_agent sequence

---

## Next Steps After Integration

Once weather is working, consider:

1. **Historical Weather**: Show "typical weather for this time of year"
2. **Multi-day Forecast**: Show 3-day forecast for planning
3. **Weather Alerts**: Show warnings (heat advisory, storm warning)
4. **Seasonal Recommendations**: Adjust "bestTime" based on historical weather
5. **Activity-Specific Gear**: Different recommendations for hiking vs. beach vs. camping

---

## Questions to Ask Me While Implementing

As you implement this, feel free to ask:

1. "How do I handle X error from the MCP server?"
2. "Should I cache weather data differently?"
3. "What should the exact tool call syntax be?"
4. "How do I debug MCP connection issues?"
5. "Can you explain how [specific part] works?"

I'm here to guide you through any implementation challenges!

---

## Summary

**What You're Building:**
- MCP weather server running as separate process
- Python MCP client connecting via stdio transport
- New Weather Agent in your sequential pipeline
- Weather + clothing recommendations for each gem
- Frontend UI displaying weather data

**Key Benefits:**
- True MCP protocol integration (standardized)
- Can swap weather providers easily
- Clean separation of concerns
- Follows your existing agent pattern

**Estimated Implementation Time:**
- Phase 1-2: 1-2 hours (MCP setup + client)
- Phase 3: 1 hour (Weather agent)
- Phase 4-5: 1 hour (Schemas + UI)
- Phase 6-7: 1 hour (Error handling + testing)
- **Total: 4-5 hours**

Good luck with the implementation! Remember - I'm here to answer questions and provide guidance as you build this. 🚀
