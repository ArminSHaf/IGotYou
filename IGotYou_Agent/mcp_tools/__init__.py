"""
MCP Tools Module - Model Context Protocol Integration

This module contains tools that connect to external MCP servers
to provide additional functionality like weather data.

The MCP (Model Context Protocol) allows our agent to communicate
with external services in a standardized way.
"""

# Export the weather tool for use by other agents
from .weather_tool import get_weather_sync, get_weather_for_location

__all__ = [
    "get_weather_sync",
    "get_weather_for_location",
]

