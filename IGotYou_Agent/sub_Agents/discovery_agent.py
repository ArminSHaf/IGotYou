from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types


try:
    from IGotYou_Agent.config import gmaps_client
except ImportError:
    print("WARNING: Could not import 'gmaps_client' from config.")
    gmaps_client = None


# 1. search Tool
def search_places_tool(query: str) -> list:
    """
    Searches for outdoor places.
    Returns ONLY the specific fields needed for the 'Hidden Gem' filter to save tokens.
    """
    if not gmaps_client:
        return [{"error": "APIKey missing"}]

    print(f"🔎 Discovery Agent searching for: '{query}'...")

    try:
        response = gmaps_client.places(
            query=query,
            type='natural_feature'
        )
        cands = []
        if response.get("status") == "OK" and "results" in response:
            for p in response['results']:
                cands.append({
                    "name": p.get('name'),
                    "place_id": p.get('place_id'),
                    "rating": p.get('rating', 0),
                    "reviews": p.get('user_ratings_total', 0),
                    # location is inside the geometry field https://developers.google.com/maps/documentation/places/web-service/legacy/search-text#maps_http_places_textsearch-txt
                    "loc": p.get('geometry', {}).get('location')
                })
        elif response.get("status") != "OK":
            print("⚠️ API returned ZERO_RESULTS / no result found.")
            return []
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
    description="Specialist in finding raw lists of outdoor locations using Google Places API.",
    instruction="""
    You are the **Discovery Agent**. 
    Use the `search_places_tool` to find raw candidates for the user's request.
    Do not filter them. Just find them.
    """,
    tools=[search_places_tool]
)
