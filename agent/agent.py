"""
IGotYou Root Agent

Main entry point for the agent system. Orchestrates a multi-agent workflow
to find hidden outdoor gems.
"""

import asyncio
from datetime import datetime

from google.adk.agents import Agent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from google.adk.runners import InMemoryRunner
from mcp import StdioServerParameters
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools import AgentTool

from .config import GOOGLE_API_KEY
from .sub_agents import analysis_agent, discovery_agent, recommendation_agent


# Current date for context-aware recommendations
current_time_str = datetime.now().strftime("%A, %B %d, %Y")

# Retry config for network resilience
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504]
)

# Weather MCP connection
weather_params = StdioServerParameters(
    command="python",
    args=["-m", "mcp_weather_server"]
)

# Hidden Gem Finder - runs sub-agents in sequence
hidden_gem_agent = SequentialAgent(
    name="Hidden_Gem_Finder",
    description="Finds hidden outdoor gems by coordinating Discovery -> Analysis -> Recommendation",
    sub_agents=[discovery_agent, analysis_agent, recommendation_agent],
)

# Root Agent - orchestrates the complete user journey
root_agent = Agent(
    name="IGOTYOU_Concierge",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    description="Orchestrates the user journey: Finds gems -> Asks User Choice -> Checks Weather -> Advises.",
    instruction=f"""
    You are the IGOTYOU Concierge - a friendly travel guide helping users discover hidden outdoor gems.
    
    Current Date: {current_time_str}
    
    WORKFLOW:
    
    STEP 1: FIND GEMS
    - Delegate the user's initial request to Hidden_Gem_Finder.
    - Present the 3 results to the user clearly.
    
    STEP 2: WAIT FOR SELECTION
    - STOP and ask the user: "Which of these 3 spots would you like to visit?"
    - Wait for their input.
    
    STEP 3: CHECK REAL WORLD DATA (MCP)
    - Once the user picks a place, identify the CITY that place is located in.
    - CRITICAL: Do NOT search weather for the specific location name 
    - CORRECT: Search weather for the CITY name (e.g., "Munich", "Berlin", "London").
    
    IMPORTANT DATE HANDLING FOR WEATHER API:
    - The weather API only supports dates within approximately 16 days into the future.
    - BEFORE calling the weather tool, check if the user's requested travel date is more than 16 days away.
    - If the date IS TOO FAR (more than ~2 weeks away), you MUST:
      1. Tell the user directly: "That's a bit too far ahead for an accurate weather forecast! 
         Weather predictions are only reliable for the next 2 weeks."
      2. DO NOT call the weather API - it will fail.
      3. Provide helpful climate info instead: Share typical/historical weather patterns for that 
         destination during their planned travel month based on your knowledge.
    - If the user's requested date IS within the next 16 days, use the Weather MCP Tool to get real forecasts.
    
    STEP 4: SYNTHESIZE & ADVISE
    - Compare the bestTime (from the gem recommendation) with the Real Weather (from the MCP tool) 
      OR general climate knowledge and suggest when is the most suitable time to go there.
    - Overlap Logic:
        - If the gem is best at "Sunset" but it's raining at sunset today, suggest the day when is not raining!
    - Outfit Advice:
        - Based on temperature (real or typical for the season), tell the user what to wear.
    """,
    tools=[AgentTool(agent=hidden_gem_agent), McpToolset(connection_params=weather_params)]
)

# Runner for executing agent queries
runner = InMemoryRunner(agent=root_agent)


async def main():
    """Run the agent in interactive mode."""
    print("I GOT YOU Agent Ready!")
    print(f"Agent: {root_agent.name}")
    print("Type 'exit' or 'quit' to stop\n")
    
    while True:
        try:
            user_input = input("You: ")
            
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            
            if not user_input.strip():
                continue
            
            print("Thinking...")
            response = await runner.run_debug(user_input)
            print(f"\nAgent: {response}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
    
    await runner.close()


if __name__ == "__main__":
    asyncio.run(main())
