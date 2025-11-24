from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types

try:
    from config import gmaps_client
except ImportError:
    print("WARNING: Could not import 'gmaps_client' from config.")
    gmaps_client = None


# 1. search Tool              TO DO BY TOMORROW
# def search_places_tool(query: str) -> list:
#     if not gmaps_client:
#         return [{"error": "APIKey missing"}]

#     print(f"🔎 Discovery Agent searching for: '{query}'...")

#     try:
#         # Use Google Places Text Search
#         results = gmaps_client.places(
#             query=query,
#             type='natural_feature' or 'point_of_interest'
#         )
#         return candidates
#     except Exception as e:
#         return [{"error": f"API Search failed: {str(e)}"}]


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
    # tools=[search_places_tool]
)
