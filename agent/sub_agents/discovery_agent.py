"""
Discovery Agent

First step in the pipeline. Searches for place candidates using Google Places API.
"""

from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types

try:
    from ..config import gmaps_client
except ImportError:
    print("Warning: Could not import gmaps_client from config")
    gmaps_client = None


def search_places_tool(query: str) -> list[dict]:
    """
    Search for outdoor places using Google Places Text Search API.
    
    Returns only the fields needed for hidden gem filtering:
    name, place_id, rating, reviews, location
    """
    if not gmaps_client:
        return [{"error": "Google Maps API key missing"}]
    
    print(f"Discovery Agent searching for: '{query}'...")
    
    try:
        response = gmaps_client.places(query=query)
        candidates = []
        
        if response.get("status") == "OK" and "results" in response:
            for place in response["results"]:
                candidates.append({
                    "name": place.get("name"),
                    "place_id": place.get("place_id"),
                    "rating": place.get("rating", 0),
                    "reviews": place.get("user_ratings_total", 0),
                    "loc": place.get("geometry", {}).get("location")
                })
        elif response.get("status") != "OK":
            print(f"API status: {response.get('status')} - no results")
            return []
        
        print(f"Found {len(candidates)} candidates")
        return candidates
        
    except Exception as e:
        print(f"Search failed: {e}")
        return [{"error": f"Search failed: {str(e)}"}]


retry_config = types.HttpRetryOptions(
    attempts=3,
    exp_base=2,
    initial_delay=1,
    http_status_codes=[429, 500, 503]
)

discovery_agent = Agent(
    name="Discovery_Agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    description="Finds raw lists of outdoor locations using Google Places API.",
    instruction="""
    You are the Discovery Agent - the first step in finding hidden outdoor gems.
    
    Use the search_places_tool to find raw candidate places for the user's request.
    Do NOT filter the results - that's the Analysis Agent's job.
    Just find them and pass them along.
    """,
    tools=[search_places_tool],
)
