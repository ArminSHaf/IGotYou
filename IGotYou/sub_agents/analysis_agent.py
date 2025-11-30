"""
Analysis Agent

Second step in the pipeline. Filters candidates by "hidden gem" criteria
and fetches detailed reviews for the top matches.

Hidden Gem Criteria:
- Review count: fewer than 300 reviews (to ensure less crowded places)
- Sorted by rating to prioritize quality
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

    1. Filters places with < 300 reviews (less crowded spots)
    2. Sorts by rating to prioritize quality
    3. Fetches detailed reviews and photos for top 3
    """
    if not gmaps_client:
        return {"status": "error", "message": "Google Maps API key missing"}
    
    if not cands or len(cands) == 0:
        return {"status": "zero_gems", "message": "No candidates to analyze"}
    
    print(f"Analyzing {len(cands)} candidates...")

    # SIMPLIFIED FILTER: Only filter by max review count (< 300)
    # This allows the agent to find more places
    MAX_REVIEW_COUNT = 300

    print(f"Filter: Places with < {MAX_REVIEW_COUNT} reviews")

    # Filter by review count only
    potential_gems = []
    for place in cands:
        review_count = place.get("reviews", 0)

        # Only requirement: fewer than 300 reviews
        if review_count < MAX_REVIEW_COUNT:
            potential_gems.append(place)

    if not potential_gems:
        print("No places met the criteria (< 300 reviews)")
        return {
            "status": "zero_gems",
            "message": f"No places found with fewer than {MAX_REVIEW_COUNT} reviews. Try a different location."
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
                fields=["name", "reviews", "url", "formatted_address", "photo", "geometry"],
                reviews_sort="most_relevant"
            )

            place_details = details.get("result", {})
            raw_reviews = place_details.get("reviews", [])
            reviews_text = [f'"{r.get("text", "")}"' for r in raw_reviews]

            # Extract photo URLs from photo references
            photo_urls = []
            photos = place_details.get("photos", [])
            if photos:
                # Get the photo reference from the first photo
                for photo in photos[:5]:  # Get up to 5 photos
                    photo_ref = photo.get("photo_reference")
                    if photo_ref:
                        # Construct photo URL using the photo reference
                        photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photoreference={photo_ref}&key={gmaps_client.key}"
                        photo_urls.append(photo_url)

            # Extract coordinates
            location = place_details.get("geometry", {}).get("location", {})
            lat = location.get("lat", gem.get("loc", {}).get("lat", 0))
            lng = location.get("lng", gem.get("loc", {}).get("lng", 0))

            result.append({
                "name": place_details.get("name", gem.get("name", "Unknown")),
                "rating": gem.get("rating", 0),
                "review_count": gem.get("reviews", 0),
                "reviews_content": "\n".join(reviews_text),
                "map_url": place_details.get("url", ""),
                "address": place_details.get("formatted_address", ""),
                "photo_urls": photo_urls if photo_urls else ["https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800"],
                "lat": lat,
                "lng": lng
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
