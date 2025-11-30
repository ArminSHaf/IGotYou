"""
IGotYou Root Agent

Main entry point for the agent system. Orchestrates a multi-agent workflow
to find hidden outdoor gems.

ARCHITECTURE OVERVIEW:
======================
This system uses a layered agent architecture:

1. Root Agent (IGOTYOU_Concierge) - The main orchestrator
   |
   ├── Intent_Understanding_Loop (LoopAgent) - Understands user's WHY
   |   └── Intent_Clarification_Agent - Asks clarifying questions
   |
   ├── Hidden_Gem_Finder (SequentialAgent) - Finds and recommends gems
   |   ├── Discovery_Agent - Searches Google Places
   |   ├── Analysis_Agent - Filters by hidden gem criteria
   |   └── Recommendation_Agent - Formats final recommendations
   |
   └── Weather MCP Tool - Gets real-time weather data

FLOW:
1. User asks for hidden gems
2. LoopAgent runs Intent_Clarification_Agent to understand WHY
3. When user intent is clear (escalate), proceed to Hidden_Gem_Finder
4. Present options and get user selection
5. Check weather for selected location
6. Provide final advice with timing and outfit recommendations
"""

import asyncio
from datetime import datetime

# ============================================================================
# GOOGLE ADK IMPORTS
# ============================================================================
# Agent: Base LLM-powered agent that can use tools and follow instructions
# SequentialAgent: Runs sub-agents one after another in order
# LoopAgent: Runs sub-agents repeatedly until escalation or max_iterations
from google.adk.agents import Agent, SequentialAgent, LoopAgent

# Gemini: Google's LLM model wrapper for ADK
from google.adk.models.google_llm import Gemini

# types: Contains configuration types like retry options
from google.genai import types

# InMemoryRunner: Simple runner that keeps conversation state in memory
from google.adk.runners import InMemoryRunner

# MCP (Model Context Protocol) tools for external integrations
from mcp import StdioServerParameters
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset

# AgentTool: Wraps an agent so it can be used as a tool by another agent
from google.adk.tools import AgentTool

# Local imports
from .config import GOOGLE_API_KEY
from .sub_agents import (
    intent_clarification_agent,  # NEW: For understanding user intent
    analysis_agent, 
    discovery_agent, 
    recommendation_agent
)


# ============================================================================
# CONFIGURATION
# ============================================================================

# Current date for context-aware recommendations
# This helps the agent understand seasonality and plan appropriately
current_time_str = datetime.now().strftime("%A, %B %d, %Y")

# Retry config for network resilience
# This prevents failures due to temporary API issues
retry_config = types.HttpRetryOptions(
    attempts=5,           # Try up to 5 times
    exp_base=7,           # Exponential backoff multiplier
    initial_delay=1,      # Start with 1 second delay
    http_status_codes=[429, 500, 503, 504]  # Retry on these HTTP errors
)


# ============================================================================
# MCP (MODEL CONTEXT PROTOCOL) CONFIGURATION
# ============================================================================
# MCP allows agents to connect to external tools/services via a standard protocol
# Here we connect to a weather server that provides real-time weather data

weather_params = StdioServerParameters(
    command="python",
    args=["-m", "mcp_weather_server"]  # This runs the weather MCP server
)


# ============================================================================
# INTENT UNDERSTANDING LOOP (NEW!)
# ============================================================================
# This LoopAgent wraps the Intent_Clarification_Agent and keeps running it
# until one of two things happens:
#   1. The agent includes "[ESCALATE]" in its response (signals it's done)
#   2. max_iterations is reached (safety limit to prevent infinite loops)
#
# WHY USE A LOOP?
# - Users often don't provide enough context in their first message
# - By looping, we can ask follow-up questions to understand their needs
# - This leads to much more personalized and relevant recommendations
# ============================================================================
intent_understanding_loop = LoopAgent(
    name="Intent_Understanding_Loop",
    description="Iteratively asks the user clarifying questions to understand what kind of hidden gem experience they're looking for. Continues until enough context is gathered.",
    sub_agents=[intent_clarification_agent],
    max_iterations=5  # Safety limit: max 5 back-and-forth exchanges
)


# ============================================================================
# HIDDEN GEM FINDER (SEQUENTIAL PIPELINE)
# ============================================================================
# This SequentialAgent runs three sub-agents in order:
#   1. Discovery -> 2. Analysis -> 3. Recommendation
#
# Each agent's output becomes the next agent's input, creating a pipeline
# that transforms a search query into polished recommendations.
# ============================================================================
hidden_gem_agent = SequentialAgent(
    name="Hidden_Gem_Finder",
    description="Finds hidden outdoor gems by coordinating Discovery -> Analysis -> Recommendation",
    sub_agents=[discovery_agent, analysis_agent, recommendation_agent],
)


# ============================================================================
# ROOT AGENT (MAIN ORCHESTRATOR)
# ============================================================================
# The Root Agent is the "brain" that coordinates everything:
#   1. First, it uses the Intent_Understanding_Loop to understand the user
#   2. Then, it uses Hidden_Gem_Finder to search for matching places
#   3. Finally, it checks weather and provides personalized advice
#
# The instruction defines the complete workflow the agent should follow.
# ============================================================================
root_agent = Agent(
    name="IGOTYOU_Concierge",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    description="Orchestrates the user journey: Understands Intent -> Finds gems -> Asks User Choice -> Checks Weather -> Advises.",
    instruction=f"""
    You are the IGOTYOU Concierge - a friendly travel guide helping users discover hidden outdoor gems.
    
    Current Date: {current_time_str}
    
    WORKFLOW:
    
    STEP 1: UNDERSTAND THE USER (NEW!)
    - When a user asks for hidden gems, FIRST delegate to Intent_Understanding_Loop.
    - This will ask the user clarifying questions to understand:
      * What TYPE of experience they want (adventure, relaxation, photography, etc.)
      * WHO they're going with (solo, couple, family, friends)
      * Any timing preferences or constraints
    - Wait for the loop to complete (it will escalate when ready).
    - The loop's output will contain a summary of what the user is looking for.
    
    STEP 2: FIND GEMS
    - Take the user intent summary from Step 1 and pass it to Hidden_Gem_Finder.
    - The finder will search for places that match their specific desires.
    - Present the 3 results to the user clearly.
    
    STEP 3: WAIT FOR SELECTION
    - STOP and ask the user: "Which of these 3 spots would you like to visit?"
    - Wait for their input.
    
    STEP 4: CHECK REAL WORLD DATA (MCP)
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
    
    STEP 5: SYNTHESIZE & ADVISE
    - Compare the bestTime (from the gem recommendation) with the Real Weather (from the MCP tool) 
      OR general climate knowledge and suggest when is the most suitable time to go there.
    - Consider the user's stated preferences from Step 1 when giving advice!
    - Overlap Logic:
        - If the gem is best at "Sunset" but it's raining at sunset today, suggest the day when is not raining!
    - Outfit Advice:
        - Based on temperature (real or typical for the season), tell the user what to wear.
        - Consider the activity type (hiking needs different gear than a peaceful garden visit)
    
    HANDLING RETURNING USERS:
    - If the user has already been through the intent clarification (you have context),
      you can skip Step 1 for follow-up requests in the same session.
    - If they ask for something completely different, run Step 1 again.
    """,
    # Tools available to this agent:
    # - Intent_Understanding_Loop: For understanding what the user really wants
    # - Hidden_Gem_Finder: For finding and recommending places
    # - Weather MCP: For real-time weather data
    tools=[
        AgentTool(agent=intent_understanding_loop),  # NEW: Intent understanding
        AgentTool(agent=hidden_gem_agent),           # Gem discovery pipeline
        McpToolset(connection_params=weather_params) # Weather data
    ]
)


# ============================================================================
# RUNNER
# ============================================================================
# The runner executes the agent and manages conversation state.
# InMemoryRunner keeps everything in memory (good for development/testing).
# For production, you might use a persistent runner that saves state to a DB.
# ============================================================================
runner = InMemoryRunner(agent=root_agent)


# ============================================================================
# MAIN FUNCTION
# ============================================================================
# Interactive CLI for testing the agent locally.
# This creates a simple chat loop where you can type messages and see responses.
# ============================================================================
async def main():
    """Run the agent in interactive mode."""
    print("=" * 60)
    print("🌟 I GOT YOU Agent Ready! 🌟")
    print("=" * 60)
    print(f"Agent: {root_agent.name}")
    print("Type 'exit' or 'quit' to stop\n")
    print("TIP: Try asking 'Find me a hidden gem in Munich'")
    print("     The agent will ask follow-up questions to understand your needs!")
    print("=" * 60 + "\n")
    
    while True:
        try:
            user_input = input("You: ")
            
            # Exit conditions
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye! Happy exploring! 🗺️")
                break
            
            # Skip empty input
            if not user_input.strip():
                continue
            
            print("🤔 Thinking...")
            response = await runner.run_debug(user_input)
            print(f"\n🎯 Agent: {response}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye! Happy exploring! 🗺️")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Clean up resources
    await runner.close()


# ============================================================================
# ENTRY POINT
# ============================================================================
# This allows running the agent directly with: python -m IGotYou.agent
# ============================================================================
if __name__ == "__main__":
    asyncio.run(main())
