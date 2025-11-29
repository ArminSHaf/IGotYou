from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types
import googlemaps

try:
    from config import gmaps_client
except ImportError:
    print("WARNING: Could not import 'gmaps_client' from config.")
    gmaps_client = None


def analysis_tool(cands: list[dict]) -> dict:
    """
    Takes a list of candidates.
    1. Filters OUT businesses (restaurants, cafes, shops).
    2. Applies hidden gem criteria (low reviews, decent rating).
    3. Sorts by rating.
    4. Fetches details for top 3.
    """
    if not gmaps_client:
        return [{"error": "APIKey missing"}]

    print(f"📊 Analysis for : '{len(cands)}' candidates...")

    # keywords that indicate a business, not a natural place
    BUSINESS_KEYWORDS = [
        'restaurant', 'cafe', 'coffee', 'hotel', 'hostel', 'inn',
        'shop', 'store', 'market', 'bar', 'pub', 'club', 'nightclub',
        'bakery', 'bistro', 'eatery', 'dining', 'diner', 'pizzeria',
        'mall', 'boutique', 'salon', 'spa', 'gym', "school", "instructor", "rental", "center"
    ]
    # google places types that are businesses
    BUSINESS_TYPES = [
        'restaurant', 'cafe', 'bar', 'food', 'meal_takeaway',
        'lodging', 'store', 'shopping_mall', 'department_store',
        'bakery', 'night_club', 'casino', 'school', 'travel_agency', 'Ski_school'
    ]

    count_reviews = 0
    for c in cands:
        count_reviews += c.get('reviews', 0)

    mean_value = count_reviews / len(cands) if cands else 0
    mean_value_over_two = mean_value / 2

    potential_hidden_gems = []
    for p in cands:
        rev = p.get('reviews', 0)
        rate = p.get('rating', 0)
        name_lower = p.get('name', '').lower()
        place_types = p.get('types', [])

        # skip if name contains business keywords
        is_business_name = any(kw in name_lower for kw in BUSINESS_KEYWORDS)
        # skip if place type is a business
        is_business_type = any(bt in place_types for bt in BUSINESS_TYPES)

        if is_business_name or is_business_type:
            print(f"  Skipping business: {p.get('name')}")
            continue

        # hidden gem criteria: 10+ reviews, below avg, decent rating
        if 10 <= rev <= mean_value_over_two and rate >= 3.5:
            potential_hidden_gems.append(p)

    if not potential_hidden_gems:
        return {
            "status": "zero_gems",
            "message": "No natural places met the hidden gem criteria."
        }

    # sort by rating
    potential_hidden_gems.sort(key=lambda x: x['rating'], reverse=True)
    top_3_gems = potential_hidden_gems[:3]

    # fetch the details for the next sub agent

    result = []
    for gem in top_3_gems:
        try:
            details = gmaps_client.place(
                place_id=gem['place_id'],
                fields=['name', 'reviews', 'url', 'formatted_address'],
                reviews_sort="most_relevant"
            )
            res = details.get('result', {})

            raw_reviews = res.get('reviews', [])
            reviews_text = []
            for r in raw_reviews:
                reviews_text.append(f"\"{r.get('text')}\"")

            result.append({
                "name": res.get('name'),
                "rating": gem['rating'],
                "review_count": gem['reviews'],
                # Text for AI to analyze
                "reviews_content": "\n".join(reviews_text),
                "map_url": res.get('url'),
                "address": res.get('formatted_address'),
            })
        except Exception as e:
            print(f"Error fetching ,{gem['name']} {e}")
    return {"status": "success", "gems": result}


# 2. Agent Configuration
retry_config = types.HttpRetryOptions(
    attempts=3,
    exp_base=2,
    initial_delay=1,
    http_status_codes=[429, 500, 503]
)

# sub agent

analysis_agent = Agent(
    name="Analysis_Agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),

    description="Filters candidates using Python logic and passes the structured data",
    instruction="""
    You are the **Analysis Agent**. 
    
    You will receive a raw list of candidates.
    
    YOUR JOB:
    1. Pass the ENTIRE list to `analysis_tool`. 
    
    2. Receive the structured data back from the tool.
    
    3. **MANDATORY STEP:** After the tool runs, you MUST repeat the JSON output as your final response.
      

    """,
    tools=[analysis_tool],
)
