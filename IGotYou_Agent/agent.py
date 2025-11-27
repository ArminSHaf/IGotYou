import asyncio

from google.adk.agents import Agent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from google.adk.runners import InMemoryRunner

# Import API key configuration
from config import GOOGLE_API_KEY

# Import specialized sub-agents for multi-agent workflow
from sub_Agents import (
    analysis_agent,
    discovery_agent,
    recommendation_agent,
)


# Robust network configuration for API calls
# This ensures reliable communication even with unstable connections
retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier for exponential backoff
    initial_delay=1,  # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504]  # Retry on these HTTP errors
)


# Main orchestrator agent that coordinates the workflow
# This is a SequentialAgent that delegates tasks to specialized sub-agents
root_agent = SequentialAgent(
    name="IGOTYOU_Agent",
    description="Your role is to manage user interaction and delegate to specialized sub-agents to find hidden outdoor gems",
    # Sub-agents are executed in sequence: Discovery → Analysis → Recommendation
    sub_agents=[
        discovery_agent,      # Finds raw candidates using Google Places API
        analysis_agent,       # Analyzes reviews and filters hidden gems
        recommendation_agent  # Formats final recommendations
    ],
)

# Create the runner instance for the agent
# This will be used to execute agent queries both in interactive and test modes
runner = InMemoryRunner(agent=root_agent)


async def main():
    """
    Main function to run the agent in interactive mode
    This function provides a REPL interface for testing the agent
    """
    print(f"✅ Agent {root_agent.name} initialized.")
    print("\n🤖 I GOT YOU Agent is ready! (Type 'exit' to quit)")
    
    while True:
        try:
            user_input = input("\nYou: ")
            
            # Allow user to exit gracefully
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye! Get you later 👋")
                break
            
            # Run the agent with the user's query
            response = await runner.run_debug(user_input)
            print(f"\nAgent: {response}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! Get you later 👋")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Clean up: close the runner when done
    await runner.close()


# Only run main() if this script is executed directly (not when imported)
# This allows the agent to be imported as a module without running the interactive mode
if __name__ == "__main__":
    asyncio.run(main())
