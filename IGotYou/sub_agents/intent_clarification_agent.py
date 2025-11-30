"""
Intent Clarification Agent

This agent is designed to understand WHY the user wants a hidden gem.
It runs inside a LoopAgent and asks clarifying questions until it has
enough context to provide personalized recommendations.

The agent uses the "escalate" mechanism to signal when it has gathered
sufficient information, which causes the LoopAgent to exit and proceed
to the next step in the pipeline.
"""

from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types


# ============================================================================
# RETRY CONFIGURATION
# ============================================================================
# Network resilience settings for API calls
# - attempts: Number of times to retry on failure
# - exp_base: Exponential backoff base (delay = initial_delay * exp_base^attempt)
# - initial_delay: Starting delay in seconds before first retry
# - http_status_codes: Which HTTP errors should trigger a retry
# ============================================================================
retry_config = types.HttpRetryOptions(
    attempts=3,
    exp_base=2,
    initial_delay=1,
    http_status_codes=[429, 500, 503]  # Rate limit, server errors
)


# ============================================================================
# INTENT CLARIFICATION AGENT
# ============================================================================
# This agent is the "interviewer" that figures out what the user really wants.
# It asks targeted questions to understand:
#   1. What TYPE of experience they want (adventure, relaxation, photography, etc.)
#   2. WHO they're going with (solo, couple, family, friends)
#   3. WHEN they want to go (time of day, season preferences)
#   4. Any CONSTRAINTS (accessibility, budget, time available)
#
# IMPORTANT: This agent uses the "escalate" keyword in its instruction.
# When the agent determines it has enough info, it responds with a message
# that includes "escalate" - this signals the LoopAgent to stop iterating.
# ============================================================================
intent_clarification_agent = Agent(
    name="Intent_Clarification_Agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    description="Quickly understands user intent for hidden gem recommendations.",
    instruction="""
    You clarify what hidden gem experience the user wants.

    Ask 1-2 quick questions to understand:
    1. Experience type (adventure, relaxation, photography, cultural)
    2. Who's going (solo, couple, family, friends)

    BE BRIEF. Ask ONE question at a time.

    ESCALATE when you have basic info OR user says "yes", "ok", "go", "sure":

    "No problem! Let me work with what I know and find you some great spots.
    [ESCALATE]"

    CRITICAL: Include "[ESCALATE]" to proceed to search.
    """
)

