from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types
import googlemaps
import os

try:
    from config import gmaps_client
except ImportError:
    print("WARNING: Could not import 'gmaps_client' from config.")
    gmaps_client = None


def analysis_tool(cands: list[dict]) -> str:
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
    # Debug: Print first candidate to check structure
    if cands:
        print(f"  [Analysis] First candidate sample: {cands[0]}")

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
            print(f"  [Analysis] Skipping business: {p.get('name')} (Type: {place_types})")
            continue
        
        print(f"  [Analysis] Checking candidate: {p.get('name')} | Rating: {rate} | Reviews: {rev}")

        # Relaxed criteria: Just check if it's not a business and has decent rating
        if rate >= 3.5:
            # Strict hidden gem check
            if 10 <= rev <= mean_value_over_two:
                p['score'] = 2 # High priority
                potential_hidden_gems.append(p)
            # Moderate hidden gem check (allow up to mean)
            elif 10 <= rev <= mean_value:
                p['score'] = 1 # Medium priority
                potential_hidden_gems.append(p)
            # Fallback (allow up to 2x mean if it's really good)
            elif rev <= mean_value * 2 and rate >= 4.5:
                p['score'] = 0 # Low priority
                potential_hidden_gems.append(p)

    if not potential_hidden_gems:
        # If still empty, just take the top rated non-businesses
        print("  [Analysis] No strict hidden gems found, falling back to top rated non-businesses.")
        for p in cands:
             rev = p.get('reviews', 0)
             rate = p.get('rating', 0)
             name_lower = p.get('name', '').lower()
             place_types = p.get('types', [])
             is_business_name = any(kw in name_lower for kw in BUSINESS_KEYWORDS)
             is_business_type = any(bt in place_types for bt in BUSINESS_TYPES)
             
             if not is_business_name and not is_business_type and rate >= 4.0:
                 p['score'] = -1
                 potential_hidden_gems.append(p)

    if not potential_hidden_gems:
        return {
            "status": "zero_gems",
            "message": "No natural places met the hidden gem criteria."
        }
    
    # Sort by score (desc) then rating (desc)
    potential_hidden_gems.sort(key=lambda x: (x.get('score', 0), x['rating']), reverse=True)
    top_3_gems = potential_hidden_gems[:3]

    result = []
    for gem in top_3_gems:
        try:
            if 'place_id' not in gem:
                print(f"  [Analysis] Skipping {gem.get('name')} - Missing place_id")
                continue
                
            details = gmaps_client.place(
                place_id=gem['place_id'],
                fields=['name', 'reviews', 'url', 'formatted_address', 'photo', 'geometry'],
                reviews_sort="most_relevant"
            )
            res = details.get('result', {})

            raw_reviews = res.get('reviews', [])
            reviews_text = []
            for r in raw_reviews:
                reviews_text.append(f"\"{r.get('text')}\"")

            # Extract photo URL
            photo_url = ""
            photos = res.get('photos', [])
            if photos:
                photo_reference = photos[0].get('photo_reference')
                if photo_reference:
                    api_key = os.environ.get("GOOGLE_MAPS_API")
                    if api_key:
                        print(f"  [DEBUG] Found API Key: {api_key[:5]}...")
                        photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photo_reference={photo_reference}&key={api_key}"
                        print(f"  [DEBUG] Generated Photo URL: {photo_url}")
                    else:
                        print("  [DEBUG] GOOGLE_MAPS_API key missing in environment variables")

            result.append({
                "name": res.get('name'),
                "rating": gem['rating'],
                "review_count": gem['reviews'],
                # Text for AI to analyze
                "reviews_content": "\n".join(reviews_text),
                "map_url": res.get('url'),
                "address": res.get('formatted_address'),
                "photo_url": photo_url,
                "coordinates": res.get('geometry', {}).get('location', {'lat': 0, 'lng': 0})
            })
        except Exception as e:
            print(f"Error fetching ,{gem['name']} {e}")
    
    print(f"[Analysis] Finished processing. Returning {len(result)} gems to Recommendation Agent.")
    import json
    return json.dumps({"status": "success", "gems": result})


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
    
    You will receive a raw list of candidates (JSON string).
    
    YOUR JOB:
    1. Pass the ENTIRE list to `analysis_tool`. 
    
    2. Receive the structured data back from the tool.
    
    3. **CRITICAL OUTPUT RULE:** 
       - You MUST output the JSON object returned by the tool EXACTLY as is.
       - Do NOT add any text.
       - Do NOT summarize.
       - Output ONLY the JSON string starting with `{`.
    """,
    tools=[analysis_tool],
)
