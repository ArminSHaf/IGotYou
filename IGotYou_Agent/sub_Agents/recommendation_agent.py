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
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="Transforms analysis agent's JSON into frontend-ready JSON format with AI-generated insights.",
    instruction="""
    You are the **Recommendation Agent**.
    
    INPUT: You will receive a JSON object (or string) containing hidden gems.
    
    **LOGIC:**
    1. Look for the "gems" key.
    2. If you find a list of places (even if the key is different), PROCESS THEM.
    3. Only return failure if the input explicitly says "status": "zero_gems".
    
    **OUTPUT FORMAT (for success):**
    {
        "gems": [
            {
                "placeName": "Name",
                "address": "Address",
                "map_url" : "URL",
                "rating": 4.5,
                "reviewCount": 100,
                "photos": ["url"],
                "coordinates": {"lat": 0, "lng": 0},
                "analysis": {
                    "whySpecial": "Why it's cool",
                    "bestTime": "When to go",
                    "insiderTip": "Tip"
                }
            }
        ]
    }
    
    **CRITICAL RULES:**
    - If you receive data, you MUST generate the JSON above.
    - If you cannot parse the input, output: "DEBUG: I received: [first 100 chars of input]"
    - Return ONLY valid JSON.
    """
)
