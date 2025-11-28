"""
Analysis Agent

Second step in the pipeline. Filters candidates by "hidden gem" criteria
and fetches detailed reviews for the top matches.

Hidden Gem Criteria:
- Review count: between 10 and (average_reviews / 2)
- Rating: at least 3.5 stars
"""

from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types

try:
    from ..config import gmaps_client
except ImportError:
    print("Warning: Could not import gmaps_client from config")
    gmaps_client = None


def analysis_tool(cands: list[dict]) -> dict:
    """
    Filter candidates and fetch details for top hidden gems.
    
    1. Filters using hidden gem criteria (low reviews, high rating)
    2. Sorts by rating
    3. Fetches detailed reviews for top 3
    """
    if not gmaps_client:
        return {"status": "error", "message": "Google Maps API key missing"}
    
    if not cands or len(cands) == 0:
        return {"status": "zero_gems", "message": "No candidates to analyze"}
    
    print(f"Analyzing {len(cands)} candidates...")
    
    # Calculate hidden gem threshold
    total_reviews = sum(c.get("reviews", 0) for c in cands)
    avg_reviews = total_reviews / len(cands)
    hidden_threshold = avg_reviews / 2
    
    print(f"Average reviews: {avg_reviews:.0f}, threshold: < {hidden_threshold:.0f}")
    
    # Filter by hidden gem criteria
    potential_gems = []
    for place in cands:
        review_count = place.get("reviews", 0)
        rating = place.get("rating", 0)
        
        # Must have 10+ reviews, less than threshold, and 3.5+ rating
        if 10 <= review_count <= hidden_threshold and rating >= 3.5:
            potential_gems.append(place)
    
    if not potential_gems:
        print("No places met the hidden gem criteria")
        return {
            "status": "zero_gems",
            "message": "No places met the hidden gem criteria. Try a broader search."
        }
    
    print(f"Found {len(potential_gems)} potential hidden gems")
    
    # Sort by rating and take top 3
    potential_gems.sort(key=lambda x: x.get("rating", 0), reverse=True)
    top_gems = potential_gems[:3]
    
    # Fetch detailed info for each gem
    result = []
    for gem in top_gems:
        try:
            details = gmaps_client.place(
                place_id=gem["place_id"],
                fields=["name", "reviews", "url", "formatted_address"],
                reviews_sort="most_relevant"
            )
            
            place_details = details.get("result", {})
            raw_reviews = place_details.get("reviews", [])
            reviews_text = [f'"{r.get("text", "")}"' for r in raw_reviews]
            
            result.append({
                "name": place_details.get("name", gem.get("name", "Unknown")),
                "rating": gem.get("rating", 0),
                "review_count": gem.get("reviews", 0),
                "reviews_content": "\n".join(reviews_text),
                "map_url": place_details.get("url", ""),
                "address": place_details.get("formatted_address", "")
            })
        except Exception as e:
            print(f"Error fetching details for {gem.get('name')}: {e}")
    
    print(f"Successfully analyzed {len(result)} hidden gems")
    return {"status": "success", "gems": result}


retry_config = types.HttpRetryOptions(
    attempts=3,
    exp_base=2,
    initial_delay=1,
    http_status_codes=[429, 500, 503]
)

analysis_agent = Agent(
    name="Analysis_Agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    description="Filters candidates using hidden gem criteria and fetches detailed reviews.",
    instruction="""
    You are the Analysis Agent - the filter in the hidden gem finding pipeline.
    
    Take the list of candidates from the Discovery Agent and filter them.
    
    1. Pass the ENTIRE list to analysis_tool
    2. Receive structured data back
    3. MANDATORY: Repeat the JSON output as your final response
    """,
    tools=[analysis_tool],
)
