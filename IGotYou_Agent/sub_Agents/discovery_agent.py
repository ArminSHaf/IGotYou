from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types


try:
    from config import gmaps_client
except ImportError:
    print("WARNING: Could not import 'gmaps_client' from config.")
    gmaps_client = None


# 1. search Tool
def search_places_tool(query: str) -> list[dict]:
    """
    Searches for outdoor NATURAL places (parks, viewpoints, trails, etc).
    Biases query toward nature spots, not businesses.
    """
    if not gmaps_client:
        return [{"error": "APIKey missing"}]

    # bias the query toward natural outdoor places
    enhanced_query = f"{query}"
    print(f"🔎 Discovery Agent searching for: '{enhanced_query}'...")

    try:
        response = gmaps_client.places(query=enhanced_query)
        cands = []
        if response.get("status") == "OK" and "results" in response:
            for p in response['results']:
                cands.append({
                    "name": p.get('name'),
                    "place_id": p.get('place_id'),
                    "rating": p.get('rating', 0),
                    "reviews": p.get('user_ratings_total', 0),
                    "loc": p.get('geometry', {}).get('location'),
                    # needed for business filtering
                    "types": p.get('types', [])
                })
        elif response.get("status") != "OK":
            print("⚠️ API returned ZERO_RESULTS / no result found.")
            return []
        print(f"Found {len(cands)} candidates")
        return cands

    except Exception as e:
        return [{"err": f"search failed {e}"}]


# 2. Agent Configuration
retry_config = types.HttpRetryOptions(
    attempts=3,
    exp_base=2,
    initial_delay=1,
    http_status_codes=[429, 500, 503]
)

# 3. The Discovery Agent Definition
discovery_agent = Agent(
    name="Discovery_Agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="Finds NATURAL outdoor locations (parks, viewpoints, trails) using Google Places API.",
    instruction="""
    You are the **Discovery Agent**. 
    Focus on NATURAL outdoor places: parks, viewpoints, gardens, trails, beaches.
    NOT businesses like restaurants, cafes, or shops.
    **CRUCIAL** refine the query in which will result landmarks and natural places - 
        e.g -> Find me a great ski resort in Sibiu -> Ski resort sibiu
    Use the `search_places_tool` to find raw candidates.
    
    **CRITICAL OUTPUT RULE:**
    1. Run the tool `search_places_tool`.
    2. The tool returns a list of objects.
    3. You MUST output that list as a valid JSON string.
    4. **IMPORTANT:** Ensure every object in the JSON has the `place_id` field. Do not omit it.
    5. Do not add any conversational text. Just the JSON.
    """,
    tools=[search_places_tool],
)
