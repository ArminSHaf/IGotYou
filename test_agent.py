#!/usr/bin/env python3
"""
IGotYou Agent Test Script

Tests the agent functionality and provides helpful error messages.
Usage: python test_agent.py
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Load environment
load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    print("ERROR: GOOGLE_API_KEY not found in environment")
    print("Check your .env file")
    sys.exit(1)

masked_key = f"{api_key[:10]}...{api_key[-4:]}" if len(api_key) > 14 else "***"
print(f"API Key loaded: {masked_key}")

print("\nNote: If you get a 403 PERMISSION_DENIED error:")
print("  1. Go to https://console.cloud.google.com/apis/library")
print("  2. Search for 'Generative Language API'")
print("  3. Enable it for your project\n")

# Import agent
try:
    from agent import root_agent, runner
    print("Agent imported successfully")
except ImportError as e:
    print(f"ERROR: Failed to import agent: {e}")
    sys.exit(1)


async def test_agent():
    """Test the agent with a sample query."""
    test_query = "Find me a hidden gem in Bucharest near Palace of Parliament"
    
    print(f"\nTesting with query: \"{test_query}\"")
    print("(This may take 30-60 seconds...)\n")
    
    try:
        response = await runner.run_debug(test_query)
        print("=" * 60)
        print("SUCCESS! Response:")
        print("=" * 60)
        print(response)
        return True
        
    except Exception as e:
        print("=" * 60)
        print("ERROR: Agent test failed")
        print("=" * 60)
        print(f"Type: {type(e).__name__}")
        print(f"Message: {str(e)}")
        
        error_str = str(e)
        if "403" in error_str or "PERMISSION_DENIED" in error_str:
            print("\nSolution: Enable 'Generative Language API' in Google Cloud Console")
        elif "401" in error_str or "UNAUTHENTICATED" in error_str:
            print("\nSolution: Check your API key is valid")
        elif "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
            print("\nSolution: Quota exceeded - wait and try again")
        
        return False
        
    finally:
        try:
            await runner.close()
        except:
            pass


if __name__ == "__main__":
    success = asyncio.run(test_agent())
    sys.exit(0 if success else 1)
