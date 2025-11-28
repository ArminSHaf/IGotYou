import asyncio
from datetime import datetime

from google.adk.agents import Agent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from google.adk.runners import InMemoryRunner
from mcp import StdioServerParameters
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools import AgentTool

# Import API key configuration
# Using relative import (.) since config.py is in the same package (IGotYou_Agent)
from .config import GOOGLE_API_KEY

# Import specialized sub-agents for multi-agent workflow
# Using relative import (.) since sub_Agents is a subpackage of IGotYou_Agent
from .sub_Agents import (
    analysis_agent,
    discovery_agent,
    recommendation_agent,
)

# Get current date/time string for agent instructions
# This helps the agent provide context-aware recommendations
current_time_str = datetime.now().strftime("%A, %B %d, %Y")


# Robust network configuration for API calls
# This ensures reliable communication even with unstable connections
retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier for exponential backoff
    initial_delay=1,  # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504]  # Retry on these HTTP errors
)

# MCP Connection for Weather
# This sets up the connection to the weather MCP server
# The server will be started as a subprocess when the agent needs weather data
weather_params = StdioServerParameters(
    command="python",
    args=["-m", "mcp_weather_server"]
)

# Hidden Gem Finder Agent (SequentialAgent)
# This agent coordinates the workflow to find hidden outdoor gems
# It delegates tasks to specialized sub-agents in sequence
hidden_gem_agent = SequentialAgent(
    name="IGOTYOU_Agent",
    description="Your role is to manage user interaction and delegate to specialized sub-agents to find hidden outdoor gems",
    # Sub-agents are executed in sequence: Discovery → Analysis → Recommendation
    sub_agents=[
        discovery_agent,      # Finds raw candidates using Google Places API
        analysis_agent,       # Analyzes reviews and filters hidden gems
        recommendation_agent  # Formats final recommendations
    ],
)

# Main Root Agent (Concierge)
# This is the top-level agent that orchestrates the complete user journey
# It combines gem finding with weather checking and provides personalized advice
root_agent = Agent(
    name="IGOTYOU_Concierge",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="Orchestrates the user journey: Finds gems -> Asks User Choice -> Checks Weather -> Advises.",
    instruction=f"""
    You are the **IGOTYOU Concierge**.
    Current Date: {current_time_str}
    
    YOUR WORKFLOW:
    
    STEP 1: FIND GEMS
    - Delegate the user's initial request to `Hidden_Gem_Finder`.
    - Present the 3 results to the user clearly.
    
    STEP 2: WAIT FOR SELECTION
    - **STOP** and ask the user: "Which of these 3 spots would you like to visit?"
    - Wait for their input.
    
    STEP 3: CHECK REAL WORLD DATA (MCP)
    - Once the user picks a place, identify the **CITY** that place is located in.
    - **CRITICAL:** Do NOT search weather for the specific location name 
    - **CORRECT:** Search weather for the CITY name in the query (e.g., "Munich", "Berlin", "London").
    
    **IMPORTANT DATE HANDLING FOR WEATHER API:**
    - The weather API only supports dates within approximately 16 days into the future.
    - **BEFORE calling the weather tool**, check if the user's requested travel date is more than 16 days away.
    - If the date IS TOO FAR (more than ~2 weeks away), you MUST:
      1. **Tell the user directly**: "That's a bit too far ahead for an accurate weather forecast! 
         Weather predictions are only reliable for the next 2 weeks."
      2. **DO NOT call the weather API** - it will fail.
      3. **Provide helpful climate info instead**: Share typical/historical weather patterns for that 
         destination during their planned travel month based on your knowledge.
      4. **Example response**: "April is a bit too far for me to get an exact forecast, but here's 
         what you can typically expect in Bali during April: temperatures around 27-30°C, 
         humidity around 80%, and occasional afternoon rain showers as it's the tail end of wet season."
    - If the user's requested date IS within the next 16 days, use the Weather MCP Tool to get real forecasts.
    
    STEP 4: SYNTHESIZE & ADVISE
    - Compare the `bestTime` (from the gem recommendation) with the `Real Weather` (from the MCP tool) 
      OR general climate knowledge and suggest when is the most suitable time to go there.
    - **Overlap Logic:**
        - If the gem is best at "Sunset" but it's raining at sunset today, suggest the day when is not raining!
    - **Outfit Advice:**
        - Based on temperature (real or typical for the season), tell the user what to wear.
    """,
    tools=[
        AgentTool(agent=hidden_gem_agent),
        McpToolset(connection_params=weather_params)
    ]
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
