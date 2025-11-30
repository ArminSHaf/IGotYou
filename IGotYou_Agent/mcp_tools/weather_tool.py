"""
MCP Weather Tool - Connects to AccuWeather via MCP Protocol

This module provides weather data for location coordinates by connecting
to the mcp-weather server (https://github.com/adhikasp/mcp-weather).

HOW IT WORKS:
1. We use the MCP Python SDK to connect to the weather server
2. The server runs as a subprocess and communicates via stdio
3. We call the weather tool with latitude/longitude coordinates
4. The server returns current weather and forecast data

FALLBACK BEHAVIOR:
- If MCP server is unavailable, we return placeholder data
- This ensures the app doesn't crash if weather isn't available
"""

import asyncio
import os
from typing import Optional


# ============================================================================
# CONFIGURATION
# ============================================================================

# Get the AccuWeather API key from environment variables
# This is used by the MCP weather server to fetch weather data
ACCUWEATHER_API_KEY = os.getenv("ACCUWEATHER_API_KEY", "")


# ============================================================================
# WEATHER DATA CACHE (Simple in-memory cache to reduce API calls)
# ============================================================================

# Dictionary to store cached weather data
# Key: "lat,lng" string, Value: (weather_data, timestamp)
_weather_cache: dict = {}

# Cache duration in seconds (1 hour = 3600 seconds)
# Weather doesn't change frequently, so caching reduces API costs
CACHE_TTL_SECONDS = 3600


# ============================================================================
# MCP WEATHER FUNCTIONS
# ============================================================================

async def get_weather_for_location(latitude: float, longitude: float) -> dict:
    """
    Fetches weather data for given coordinates using MCP weather server.
    
    This is the main async function that connects to the MCP server
    and retrieves weather information.
    
    Args:
        latitude: The latitude coordinate (e.g., 37.7749 for San Francisco)
        longitude: The longitude coordinate (e.g., -122.4194 for San Francisco)
    
    Returns:
        dict: Weather data with the following structure:
            {
                "temperature": float or None,  # Temperature in Fahrenheit
                "conditions": str,             # Weather description
                "humidity": int or None,       # Humidity percentage
                "hasPrecipitation": bool       # Whether it's raining/snowing
            }
    
    Example:
        >>> weather = await get_weather_for_location(37.7749, -122.4194)
        >>> print(weather["temperature"])  # 68.5
        >>> print(weather["conditions"])   # "Partly cloudy"
    """
    import time
    
    # ========================================================================
    # CHECK CACHE FIRST (to reduce API calls and save money)
    # ========================================================================
    
    # Create a cache key from coordinates (rounded to 4 decimal places)
    cache_key = f"{latitude:.4f},{longitude:.4f}"
    current_time = time.time()
    
    # Check if we have cached data that's still valid
    if cache_key in _weather_cache:
        cached_data, cached_timestamp = _weather_cache[cache_key]
        # If cache is still fresh (less than CACHE_TTL_SECONDS old)
        if current_time - cached_timestamp < CACHE_TTL_SECONDS:
            print(f"✅ Using cached weather for coordinates: {cache_key}")
            return cached_data
    
    # ========================================================================
    # TRY TO CONNECT TO MCP WEATHER SERVER
    # ========================================================================
    
    try:
        # Import MCP libraries - these connect us to the weather server
        from mcp import ClientSession, StdioServerParameters, stdio_client
        
        # Check if we have the API key configured
        if not ACCUWEATHER_API_KEY:
            print("⚠️ ACCUWEATHER_API_KEY not set - returning fallback weather")
            return _get_fallback_weather()
        
        # Configure the MCP server connection parameters
        # This tells Python how to start and connect to the weather server
        server_params = StdioServerParameters(
            command="uvx",  # Use uvx to run the server (similar to npx for Python)
            args=["mcp-weather"],  # The package name to run
            env={
                # Pass the API key to the server process
                "ACCUWEATHER_API_KEY": ACCUWEATHER_API_KEY,
                # Preserve PATH so uvx can find Python
                "PATH": os.environ.get("PATH", ""),
            }
        )
        
        print(f"🌤️ Fetching weather for coordinates: {latitude}, {longitude}")
        
        # Connect to the MCP server via stdio (standard input/output)
        # The 'async with' ensures proper cleanup when we're done
        async with stdio_client(server_params) as (read_stream, write_stream):
            # Create a session to communicate with the server
            async with ClientSession(read_stream, write_stream) as session:
                # Initialize the connection (required handshake)
                await session.initialize()
                
                # List available tools to find the weather tool name
                tools_result = await session.list_tools()
                print(f"📋 Available MCP tools: {[t.name for t in tools_result.tools]}")
                
                # Call the weather tool with our coordinates
                # Note: The actual tool name might vary - check mcp-weather docs
                result = await session.call_tool(
                    name="get_weather",  # Tool name from mcp-weather
                    arguments={
                        "latitude": latitude,
                        "longitude": longitude
                    }
                )
                
                # Parse the result from the MCP server
                # The result.content contains the weather data
                weather_data = _parse_mcp_result(result.content)
                
                # Cache the result for future requests
                _weather_cache[cache_key] = (weather_data, current_time)
                
                print(f"✅ Weather fetched successfully: {weather_data['conditions']}")
                return weather_data
                
    except ImportError as e:
        # MCP library not installed
        print(f"⚠️ MCP library not installed: {e}")
        print("   Install with: pip install mcp")
        return _get_fallback_weather()
        
    except Exception as e:
        # Any other error (server not running, network issues, etc.)
        print(f"❌ Error fetching weather from MCP server: {e}")
        print("   Returning fallback weather data...")
        return _get_fallback_weather()


def _parse_mcp_result(content) -> dict:
    """
    Parses the raw MCP result into our standard weather format.
    
    The MCP server might return data in various formats, so we
    normalize it here to match what our frontend expects.
    
    Args:
        content: Raw content from MCP server (could be string, dict, or list)
    
    Returns:
        dict: Normalized weather data
    """
    try:
        # The content might be a list with one item, or a dict directly
        if isinstance(content, list) and len(content) > 0:
            # Get the first item if it's a list
            data = content[0]
            # If it has a 'text' field (common in MCP), parse that
            if hasattr(data, 'text'):
                import json
                data = json.loads(data.text)
        elif isinstance(content, dict):
            data = content
        else:
            # Try to parse as JSON string
            import json
            data = json.loads(str(content))
        
        # Extract the fields we need, with sensible defaults
        current = data.get("current", data)
        
        return {
            "temperature": current.get("temperature") or current.get("Temperature", {}).get("Value"),
            "conditions": current.get("description") or current.get("WeatherText", "Unknown"),
            "humidity": current.get("humidity") or current.get("RelativeHumidity"),
            "hasPrecipitation": current.get("hasPrecipitation") or current.get("HasPrecipitation", False)
        }
        
    except Exception as e:
        print(f"⚠️ Error parsing MCP result: {e}")
        return _get_fallback_weather()


def _get_fallback_weather() -> dict:
    """
    Returns fallback weather data when MCP server is unavailable.
    
    This ensures the application continues to work even if weather
    data can't be fetched. The UI will show "Weather unavailable".
    
    Returns:
        dict: Placeholder weather data
    """
    return {
        "temperature": None,
        "conditions": "Weather unavailable",
        "humidity": None,
        "hasPrecipitation": False
    }


# ============================================================================
# SYNCHRONOUS WRAPPER (Required for Google ADK tools)
# ============================================================================

def get_weather_sync(latitude: float, longitude: float) -> dict:
    """
    Synchronous wrapper for get_weather_for_location.
    
    Google ADK agent tools need synchronous functions, but our MCP
    client is async. This wrapper handles the async-to-sync conversion.
    
    Args:
        latitude: The latitude coordinate
        longitude: The longitude coordinate
    
    Returns:
        dict: Weather data (same format as get_weather_for_location)
    
    Usage in agent tools:
        def my_weather_tool(lat: float, lng: float) -> dict:
            return get_weather_sync(lat, lng)
    """
    try:
        # Try to get the current event loop
        loop = asyncio.get_event_loop()
        
        # If the loop is running (common in async contexts), we need special handling
        if loop.is_running():
            # Create a new loop in a separate thread
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(
                    asyncio.run,
                    get_weather_for_location(latitude, longitude)
                )
                return future.result(timeout=30)  # 30 second timeout
        else:
            # Loop exists but isn't running - use it directly
            return loop.run_until_complete(
                get_weather_for_location(latitude, longitude)
            )
            
    except RuntimeError:
        # No event loop exists - create one
        return asyncio.run(get_weather_for_location(latitude, longitude))


# ============================================================================
# TEST FUNCTION (for development/debugging)
# ============================================================================

async def _test_weather():
    """
    Test function to verify the weather tool is working.
    
    Run this directly to test: python weather_tool.py
    """
    # Test with San Francisco coordinates
    sf_lat, sf_lng = 37.7749, -122.4194
    
    print("=" * 50)
    print("🧪 Testing MCP Weather Tool")
    print("=" * 50)
    print(f"📍 Test location: San Francisco ({sf_lat}, {sf_lng})")
    
    weather = await get_weather_for_location(sf_lat, sf_lng)
    
    print("\n📊 Results:")
    print(f"   Temperature: {weather['temperature']}°F")
    print(f"   Conditions: {weather['conditions']}")
    print(f"   Humidity: {weather['humidity']}%")
    print(f"   Precipitation: {weather['hasPrecipitation']}")
    print("=" * 50)


# Run test if this file is executed directly
if __name__ == "__main__":
    asyncio.run(_test_weather())

