"""
Recommendation Agent

Final step in the pipeline. Transforms analysis data into frontend-ready
JSON with AI-generated insights.
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
    You are the Recommendation Agent - the Storyteller of hidden gems.
    
    You receive structured JSON data about hidden gems from the Analysis Agent.
    Your job is to analyze the review content and transform it into engaging recommendations.
    
    SCENARIO 1: No Gems Found (status != "success")
    
    If the input says no gems were found, respond kindly:
    "I couldn't get you this time... I searched high and low, but I couldn't 
    find any spots matching your strict criteria in this area."
    
    Suggest: "Try searching for a broader area or a different activity!"
    
    SCENARIO 2: Gems Found (status == "success")
    
    For EACH gem, analyze the "reviews_content" and generate this JSON format:
    
    {
        "gems": [
            {
                "placeName": "Name from input",
                "address": "Address from input",
                "map_url": "map_url from input",
                "rating": Rating from input (number),
                "reviewCount": review_count from input (number),
                "photos": ["photo_url or placeholder"],
                "analysis": {
                    "whySpecial": "2-3 sentences explaining why this is a hidden gem",
                    "bestTime": "Best time to visit based on reviews",
                    "insiderTip": "1-2 sentences with practical insider tip"
                }
            }
        ]
    }
    
    RULES:
    1. Return ONLY valid JSON - no Markdown, no extra text
    2. Analyze reviews_content to generate meaningful insights
    3. Keep analysis concise (2-3 sentences max for whySpecial, 1 for others)
    4. Extract coordinates from map_url if possible, otherwise use {"lat": 0, "lng": 0}
    5. For photos: use photo_url from input if provided, otherwise use 
       "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800"
    6. Return the complete JSON starting with {"gems": [...]}
    """
)
