from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types
import googlemaps

try:
    from IGotYou_Agent.config import gmaps_client
except ImportError:
    print("WARNING: Could not import 'gmaps_client' from config.")
    gmaps_client = None


def analysis_tool(cands: list) -> dict:
    """
    Takes a raw list of candidates.
    1. Filters them using Python (Reviews < 300, Rating > 4.0).
    2. Sorts by rating.
    3. Fetches details (reviews) for the top 3 'survivors'.
    """
    if not gmaps_client:
        return [{"error": "APIKey missing"}]

    print(f"📊 Analysis for : '{len(cands)}' candidates...")

    potential_hidden_gems = []
    for p in cands:
        rev = p.get('reviews')
        rate = p.get('rating')

        if 10 <= rev <= 400 and rate >= 3.5:
            potential_hidden_gems.append(p)

    if not potential_hidden_gems:
        return {
            "no potential hidden gems"
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

    description="Filters candidates using Python logic and analyzes reviews.",
    instruction="""
    You are the **Analysis Agent**. 
    
    INPUT: You will receive a raw JSON list of candidates.
    
    YOUR JOB:
    1. Pass the ENTIRE list to `analyze_hidden_gems_tool`. 
       (Do not filter it yourself. The tool does the math).
    
    2. Receive the structured data back from the tool.
    
    3. For each Gem returned by the tool, write a short analysis:
       - **Why it's special**: Based on the `reviews_content`.
       - **Insider Tip**: Extract one specific tip. Time Interval to visit if there is any.
       
    OUTPUT: Return the final structured JSON with your analysis added.
    """,
    tools=[analysis_tool]
)
