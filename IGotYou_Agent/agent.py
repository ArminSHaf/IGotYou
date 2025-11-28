import asyncio
from datetime import datetime

from google.adk.agents import Agent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from google.adk.runners import InMemoryRunner
from mcp import StdioServerParameters
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools import AgentTool

from config import GOOGLE_API_KEY
from sub_Agents import (
    analysis_agent,
    discovery_agent,
    recommendation_agent,
)

current_time_str = datetime.now().strftime("%A, %B %d, %Y")


# Robust network configuration
retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,  # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504]  # Retry on these HTTP errors
)

# MCP Connection for Weather
weather_params = StdioServerParameters(
    command="python",
    args=["-m", "mcp_weather_server"]
)


hidden_gem_agent = SequentialAgent(
    name="IGOTYOU_Agent",
    description="Your role is to manages user interaction and delegates to specialized sub-agents",
    sub_agents=[
        discovery_agent,
        analysis_agent,
        recommendation_agent
    ],
)

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
    - **CORRECT:** Search weather for the CITY  name in the query (e.g., "Munich", "Berlin", "London").
    - Use the provided Weather MCP Tool to search for that **CITY's** forecast for the next 5 days.
    
    STEP 4: SYNTHESIZE & ADVISE
    - Compare the `bestTime` (from the gem recommendation) with the `Real Weather` (from the MCP tool) and suggest when is the most suitable time to go there.
    - **Overlap Logic:**
        - If the gem is best at "Sunset" but it's raining at sunset today, suggest the day when is not raining!
    - **Outfit Advice:**
        - Check the temperature. Tell the user exactly what to wear (e.g., "It's 12°C, bring a light jacket").
    """,
    tools=[
        AgentTool(agent=hidden_gem_agent),
        McpToolset(connection_params=weather_params)
    ]
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
