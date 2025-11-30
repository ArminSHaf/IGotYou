"""
IGotYou Agent Package

Multi-agent system for discovering hidden outdoor gems using Google ADK.

Architecture:
  Root Agent (Concierge)
    |
    +-- Hidden Gem Finder (Sequential)
    |     +-- Discovery Agent   -> searches Google Places
    |     +-- Analysis Agent    -> filters by hidden gem criteria
    |     +-- Recommendation Agent -> generates insights
    |
    +-- Weather MCP Tool

Usage:
    from agent import root_agent, runner
    response = await runner.run_debug("Find a hidden beach in Bali")
"""

from .agent import root_agent, runner

__all__ = ["root_agent", "runner"]
