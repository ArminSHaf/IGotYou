"""
Recommendation Agent

Final step in the pipeline. Transforms analysis data into frontend-ready
JSON with AI-generated insights.

OPTIMIZED VERSION: No external image searches - uses only Google Places photos
for faster response times.
"""

from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types

retry_config = types.HttpRetryOptions(
    attempts=3,
    exp_base=2,
    initial_delay=1,
    http_status_codes=[429, 500, 503]
)

recommendation_agent = Agent(
    name="Recommendation_Agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    description="Transforms analysis data into frontend-ready JSON with AI insights.",
    instruction="""
    You are the Recommendation Agent - transform analysis data into engaging JSON.

    INPUT: JSON with gem data from Analysis Agent
    OUTPUT: Frontend-ready JSON with insights

    If no gems found (status != "success"):
    "I couldn't find any spots matching your criteria in this area. Try a broader search!"

    If gems found (status == "success"), generate this JSON:

    {
        "gems": [
            {
                "placeName": "name from input",
                "address": "address from input",
                "coordinates": {"lat": lat, "lng": lng},
                "rating": rating (number),
                "reviewCount": review_count (number),
                "photos": photo_urls from input (array),
                "analysis": {
                    "whySpecial": "2-3 sentences why this is a hidden gem",
                    "bestTime": "Best time to visit",
                    "insiderTip": "Practical tip"
                }
            }
        ]
    }

    RULES:
    1. Return ONLY valid JSON - no Markdown, no extra text
    2. Use reviews_content to generate insights
    3. Keep analysis concise
    4. Use lat/lng from input as coordinates {lat: number, lng: number}
    5. Use photo_urls array from input (already from Google Places API)
    """,
    tools=[]  # No tools needed - faster execution
)
