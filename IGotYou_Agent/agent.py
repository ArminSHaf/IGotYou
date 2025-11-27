import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types
import asyncio

load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    raise ValueError(
        "GOOGLE_API_KEY not found.set it in .env file / environment")


retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,  # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504]  # Retry on these HTTP errors
)

root_agent = Agent(
    name="IGOTYOU_Agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="Your role is to helps travelers discover quiet, lesser-known outdoor destinations",
    instruction="""
        Your role is to find hidden outdoor gems with fewer than 300 reviews and at least a 4.0 rating.
        Analyze top reviews to explain why the place is special, the best time to visit, and one insider tip.
        Always return 2–3 recommendations in a clear, structured JSON format.

        IMPORTANT: Your response MUST be a valid JSON object with this exact structure:
        {
            "gems": [
                {
                    "placeName": "Name of the place",
                    "address": "Full address",
                    "coordinates": {"lat": 0.0, "lng": 0.0},
                    "rating": 4.5,
                    "reviewCount": 150,
                    "photos": ["photo_url_1", "photo_url_2"],
                    "analysis": {
                        "whySpecial": "Why this place is special based on reviews",
                        "bestTime": "Best time to visit",
                        "insiderTip": "One insider tip"
                    }
                }
            ]
        }

        Use Google Search to find real places with actual coordinates, ratings, and review counts.
        For photos, use publicly available image URLs from search results or use placeholder images.
        Always return valid JSON that can be parsed directly.
    """,
    tools=[google_search],
)


# Create the runner instance for the agent
# This will be used to execute agent queries
runner = InMemoryRunner(agent=root_agent)


async def main():
    """
    Main function to test the agent
    This function runs a sample query to test the agent functionality
    """
    # Test query: Find hidden gems in Bucharest near Palace of Parliament
    response = await runner.run_debug(
        "Find me a hidden gem in Campeche Mexico"
    )
    print(response)

    # Clean up: close the runner when done
    await runner.close()


# Only run main() if this script is executed directly (not when imported)
# This allows the agent to be imported as a module without running the test
if __name__ == "__main__":
    asyncio.run(main())
