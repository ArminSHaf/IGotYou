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
        Always return 2–3 recommendations in a clear, structured format with name, rating, review count, analysis, and coordinates.
    """,
    tools=[google_search],
)


runner = InMemoryRunner(agent=root_agent)


async def main():
    response = await runner.run_debug(
        "Find me a hidden gem in Bucharest near Palace of Parliament"
    )
    print(response)

    await runner.close()

asyncio.run(main())
