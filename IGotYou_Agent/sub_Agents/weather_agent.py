"""
Weather Agent - Enriches Hidden Gems with Weather Data & Clothing Recommendations

This agent is the FINAL step in our agent pipeline. It takes the gems from
the Recommendation Agent and adds:
1. Current weather conditions for each location
2. AI-generated clothing recommendations based on the weather

HOW IT WORKS:
1. Receives JSON with gems (each gem has coordinates)
2. For each gem, calls the MCP weather tool to get weather data
3. Uses Gemini AI to generate smart clothing recommendations
4. Returns enriched gems with weather + clothing info

PIPELINE POSITION:
    Discovery → Analysis → Recommendation → Weather (YOU ARE HERE)
"""

from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types

# Import the weather tool from our MCP tools module
from ..mcp_tools.weather_tool import get_weather_sync


# ============================================================================
# RETRY CONFIGURATION (for API resilience)
# ============================================================================

# Configure retry behavior for Gemini API calls
# This helps handle temporary network issues or rate limits
retry_config = types.HttpRetryOptions(
    attempts=3,              # Retry up to 3 times
    exp_base=2,              # Exponential backoff multiplier
    initial_delay=1,         # Wait 1 second before first retry
    http_status_codes=[      # Retry on these HTTP errors:
        429,                 # - 429: Rate limited (too many requests)
        500,                 # - 500: Server error
        503                  # - 503: Service unavailable
    ]
)


# ============================================================================
# WEATHER ENRICHMENT TOOL
# ============================================================================

def enrich_gems_with_weather(gems_json: str) -> dict:
    """
    Enriches gem data with weather information from MCP weather server.
    
    This tool is called by the Weather Agent to fetch weather data
    for each hidden gem's coordinates.
    
    Args:
        gems_json: JSON string containing gems data from Recommendation Agent
                   Expected format: {"gems": [...]}
    
    Returns:
        dict: Same gems structure with added "weather" field for each gem
              {
                  "gems": [
                      {
                          "placeName": "...",
                          "coordinates": {"lat": 37.7, "lng": -122.4},
                          "weather": {
                              "temperature": 68,
                              "conditions": "Partly Cloudy",
                              "humidity": 55,
                              "hasPrecipitation": false
                          },
                          ...
                      }
                  ]
              }
    
    IMPORTANT: This tool handles errors gracefully - if weather can't be
    fetched for a gem, it adds placeholder weather data instead of failing.
    """
    import json
    
    print("\n🌤️ Weather Agent: Enriching gems with weather data...")
    
    # ========================================================================
    # PARSE INPUT JSON
    # ========================================================================
    
    try:
        # Handle both string and dict input
        if isinstance(gems_json, str):
            # Remove markdown code blocks if present (from LLM output)
            clean_json = gems_json.strip()
            if clean_json.startswith("```"):
                # Extract JSON from markdown code block
                lines = clean_json.split("\n")
                # Remove first line (```json) and last line (```)
                clean_json = "\n".join(lines[1:-1])
            
            data = json.loads(clean_json)
        else:
            data = gems_json
            
        gems = data.get("gems", [])
        
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing gems JSON: {e}")
        # Return empty gems array to match expected return type {"gems": [...]}
        # This ensures the Weather Agent receives the expected structure
        return {"gems": []}
    
    # ========================================================================
    # FETCH WEATHER FOR EACH GEM
    # ========================================================================
    
    enriched_gems = []
    
    for i, gem in enumerate(gems):
        print(f"   📍 Processing gem {i+1}/{len(gems)}: {gem.get('placeName', 'Unknown')}")
        
        try:
            # Extract coordinates from the gem
            # Coordinates can be in different formats depending on the source
            coords = gem.get("coordinates", {})
            
            # Handle different coordinate formats
            if isinstance(coords, dict):
                lat = coords.get("lat") or coords.get("latitude")
                lng = coords.get("lng") or coords.get("longitude")
            else:
                lat = None
                lng = None
            
            # If no coordinates, try to extract from map_url
            if (not lat or not lng) and gem.get("map_url"):
                lat, lng = _extract_coords_from_url(gem.get("map_url"))
            
            # ================================================================
            # CALL MCP WEATHER SERVICE
            # ================================================================
            
            if lat and lng:
                # Fetch weather using our MCP tool
                weather = get_weather_sync(float(lat), float(lng))
                gem["weather"] = weather
                print(f"      ✅ Weather: {weather.get('conditions', 'N/A')}")
            else:
                # No coordinates available - use placeholder
                print(f"      ⚠️ No coordinates - skipping weather")
                gem["weather"] = {
                    "temperature": None,
                    "conditions": "Location unavailable",
                    "humidity": None,
                    "hasPrecipitation": False
                }
            
            # Also ensure coordinates are in the gem (for frontend map)
            if lat and lng and "coordinates" not in gem:
                gem["coordinates"] = {"lat": float(lat), "lng": float(lng)}
                
        except Exception as e:
            # Handle any errors gracefully - don't let one gem break everything
            print(f"      ❌ Error fetching weather: {e}")
            gem["weather"] = {
                "temperature": None,
                "conditions": "Weather unavailable",
                "humidity": None,
                "hasPrecipitation": False
            }
        
        enriched_gems.append(gem)
    
    print(f"✅ Weather enrichment complete for {len(enriched_gems)} gems\n")
    
    return {"gems": enriched_gems}


def _extract_coords_from_url(map_url: str) -> tuple:
    """
    Extracts latitude and longitude from a Google Maps URL.
    
    Google Maps URLs contain coordinates in various formats:
    - https://maps.google.com/?q=37.7749,-122.4194
    - https://goo.gl/maps/... (shortened, can't extract directly)
    
    Args:
        map_url: A Google Maps URL string
    
    Returns:
        tuple: (latitude, longitude) or (None, None) if extraction fails
    """
    import re
    
    if not map_url:
        return None, None
    
    try:
        # Try to find coordinates in the URL
        # Pattern matches: q=37.7749,-122.4194 or @37.7749,-122.4194
        patterns = [
            r'[?&]q=(-?\d+\.?\d*),(-?\d+\.?\d*)',  # ?q=lat,lng
            r'@(-?\d+\.?\d*),(-?\d+\.?\d*)',        # @lat,lng
            r'place/(-?\d+\.?\d*),(-?\d+\.?\d*)',   # place/lat,lng
        ]
        
        for pattern in patterns:
            match = re.search(pattern, map_url)
            if match:
                lat = float(match.group(1))
                lng = float(match.group(2))
                return lat, lng
                
    except Exception as e:
        print(f"      ⚠️ Could not extract coords from URL: {e}")
    
    return None, None


# ============================================================================
# WEATHER AGENT DEFINITION
# ============================================================================

weather_agent = Agent(
    name="Weather_Agent",
    
    # Use a lightweight model for fast responses
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    
    # Short description for the orchestrator agent
    description="Enriches hidden gems with real-time weather data and clothing recommendations",
    
    # Detailed instructions for the agent's behavior
    instruction="""
    You are the **Weather Agent** - the final step in our hidden gem discovery pipeline!
    
    ═══════════════════════════════════════════════════════════════
    YOUR MISSION:
    ═══════════════════════════════════════════════════════════════
    
    1. FIRST: Take the gems JSON from the previous agent and call `enrich_gems_with_weather`
       This will add current weather data to each gem.
    
    2. THEN: For EACH gem that has weather data, generate a "clothingRecommendation"
       Add this to the gem's "analysis" section.
    
    ═══════════════════════════════════════════════════════════════
    CLOTHING RECOMMENDATION GUIDELINES:
    ═══════════════════════════════════════════════════════════════
    
    Based on the weather conditions, suggest appropriate clothing:
    
    🌡️ TEMPERATURE BASED:
       - Hot (>85°F): Light, breathable fabrics, shorts, t-shirt, sunhat
       - Warm (70-85°F): Light layers, comfortable walking clothes
       - Cool (55-70°F): Light jacket or sweater, long pants
       - Cold (<55°F): Warm jacket, layers, warm pants
    
    ☀️ CONDITION BASED:
       - Sunny: Sunglasses, sunscreen, hat
       - Cloudy: Light layers (weather can change)
       - Rainy: Waterproof jacket, umbrella, water-resistant shoes
       - Windy: Windbreaker, secure hat
    
    🥾 ACTIVITY BASED (based on gem type):
       - Hiking trails: Sturdy shoes, moisture-wicking clothes
       - Beaches: Swimwear, sandals, cover-up
       - Mountain areas: Layers (temperature varies with altitude)
    
    ═══════════════════════════════════════════════════════════════
    OUTPUT FORMAT:
    ═══════════════════════════════════════════════════════════════
    
    Return ONLY valid JSON with this structure:
    {
        "gems": [
            {
                "placeName": "...",
                "address": "...",
                "coordinates": {"lat": ..., "lng": ...},
                "rating": ...,
                "reviewCount": ...,
                "photos": [...],
                "weather": {
                    "temperature": 72,
                    "conditions": "Partly Cloudy",
                    "humidity": 55,
                    "hasPrecipitation": false
                },
                "analysis": {
                    "whySpecial": "...",
                    "bestTime": "...",
                    "insiderTip": "...",
                    "clothingRecommendation": "Wear light, breathable clothing and bring sunscreen. A hat and sunglasses are essential for the sunny trail."
                }
            }
        ]
    }
    
    ═══════════════════════════════════════════════════════════════
    CRITICAL RULES:
    ═══════════════════════════════════════════════════════════════
    
    ✅ DO:
       - Return ONLY valid JSON (no markdown, no explanations)
       - Keep clothingRecommendation to 1-2 sentences
       - Include ALL fields from the input (don't remove anything)
       - Make recommendations practical and specific
    
    ❌ DON'T:
       - Add markdown formatting (no ```)
       - Skip any gems (process all of them)
       - Make recommendations without checking weather data
       - Change existing analysis content (whySpecial, bestTime, insiderTip)
    """,
    
    # Register our weather enrichment tool
    tools=[enrich_gems_with_weather],
)

