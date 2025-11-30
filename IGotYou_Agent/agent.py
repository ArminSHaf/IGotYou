import asyncio
from datetime import datetime

from google.adk.agents import Agent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from google.adk.runners import InMemoryRunner
from mcp import StdioServerParameters
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools import AgentTool

try:
    # 1. For Pytest
    from .config import GOOGLE_API_KEY
    from .sub_Agents import (
        analysis_agent,
        discovery_agent,
        recommendation_agent,
    )
except ImportError:
    # 2. For 'python agent.py'
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
    
    YOUR WORKFLOW:
    
    **PHASE 1: DISCOVERY (User asks for a place)**
    - If the user asks for a recommendation (e.g., "hiking in Alps", "hidden beach"), delegate to `Hidden_Gem_Finder`.
    - **CRITICAL:** The `Hidden_Gem_Finder` will return a JSON object with gems. You MUST output this JSON object EXACTLY as is.
    - **DO NOT** add any conversational text, questions, or summaries.
    - **DO NOT** ask "Which one do you like?". Just return the JSON.
    
    **PHASE 2: SELECTION & ADVICE (User says "I choose [Place Name]")**
    - If the user selects a place (e.g., "I choose Indjánagil"), proceed to check weather and give advice.
    - **STEP A: Identify City**
        - Identify the **CITY** the place is located in.
    - **STEP B: Check Weather (MCP)**
        - Use the Weather MCP Tool to search for that **CITY's** forecast for the next 3 days from TODAY ({current_time_str}).
        - Ensure start_date is TODAY.
    - **STEP C: Synthesize & Advise**
        - Compare `bestTime` with `Real Weather`.
        - Provide Outfit Advice based on temperature.
    - **CRITICAL OUTPUT FOR PHASE 2:**
        - Return the advice in this JSON format ONLY:
        {{
            "summary": "Brief summary of weather and best time.",
            "outfit": "Specific outfit advice.",
            "best_time_match": "Recommended day/time."
        }}

    **PHASE 3: CONVERSATION (User asks follow-up)**
    - If the user asks a follow-up question (e.g., "What should I wear?", "Is it kid friendly?"), answer in PLAIN TEXT.
    - Do NOT use JSON for follow-up conversation.
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
