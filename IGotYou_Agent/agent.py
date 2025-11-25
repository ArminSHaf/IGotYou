import asyncio

from google.adk.agents import Agent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from google.adk.runners import InMemoryRunner

from config import GOOGLE_API_KEY
from sub_Agents import (
    analysis_agent,
    discovery_agent,
    recommendation_agent,
)


# Robust network configuration
retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,  # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504]  # Retry on these HTTP errors
)


root_agent = SequentialAgent(
    name="IGOTYOU_Agent",
    description="Your role is to manages user interaction and delegates to specialized sub-agents",
    sub_agents=[
        discovery_agent,
        analysis_agent,
        recommendation_agent
    ],
)

# engine of the agent
if __name__ == "__main__":
    print(f"✅ Agent {root_agent.name} initialized.")

    async def main():
        runner = InMemoryRunner(agent=root_agent)
        print("\n🤖 I GOT YOU Agent is ready! (Type 'exit' to quit)")

        while True:
            try:
                user_input = input("\nYou: ")

                if user_input.lower() in ["exit", "quit"]:
                    print("Goodbye! Get you later 👋")
                    break
                response = await runner.run_debug(user_input)
                print(f"\nAgent: {response}")
            except Exception as e:
                print(f"Error: {e}")

    asyncio.run(main())
