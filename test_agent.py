#!/usr/bin/env python3
"""
Test script for IGotYou Agent
This script tests the agent functionality and provides helpful error messages
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check if API key is loaded
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    print("❌ ERROR: GOOGLE_API_KEY not found in environment variables")
    print("   Please check your .env file and ensure it contains:")
    print("   GOOGLE_API_KEY=your_api_key_here")
    sys.exit(1)

print(f"✅ API Key loaded: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else '***'}")

# Check if API key needs to be enabled
print("\n⚠️  NOTE: If you get a 403 PERMISSION_DENIED error:")
print("   1. Go to: https://console.cloud.google.com/apis/library")
print("   2. Search for 'Generative Language API'")
print("   3. Enable it for your project")
print("   4. Make sure your API key has access to this API\n")

# Try to import the agent
try:
    from IGotYou_Agent.agent import root_agent, runner
    print("✅ Agent imported successfully")
except ImportError as e:
    print(f"❌ ERROR: Failed to import agent: {e}")
    sys.exit(1)

# Test function
async def test_agent():
    """Test the agent with a sample query"""
    print("\n🚀 Testing agent with query: 'Find me a hidden gem in Bucharest near Palace of Parliament'")
    print("   (This may take 30-60 seconds...)\n")
    
    try:
        response = await runner.run_debug(
            "Find me a hidden gem in Bucharest near Palace of Parliament"
        )
        print("\n" + "="*60)
        print("✅ SUCCESS! Agent response received:")
        print("="*60)
        print(response)
        print("="*60)
        return True
    except Exception as e:
        print("\n" + "="*60)
        print("❌ ERROR: Agent test failed")
        print("="*60)
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("="*60)
        
        # Provide helpful error messages
        if "403" in str(e) or "PERMISSION_DENIED" in str(e):
            print("\n💡 SOLUTION:")
            print("   Your API key is blocked or doesn't have the right permissions.")
            print("   Steps to fix:")
            print("   1. Visit: https://console.cloud.google.com/apis/library")
            print("   2. Search and enable 'Generative Language API'")
            print("   3. Visit: https://console.cloud.google.com/apis/credentials")
            print("   4. Check your API key restrictions")
            print("   5. Ensure 'Generative Language API' is allowed")
        elif "401" in str(e) or "UNAUTHENTICATED" in str(e):
            print("\n💡 SOLUTION:")
            print("   Your API key is invalid or expired.")
            print("   1. Check your .env file has the correct API key")
            print("   2. Get a new key from: https://makersuite.google.com/app/apikey")
        elif "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            print("\n💡 SOLUTION:")
            print("   API quota exceeded. Please wait and try again later.")
        
        return False
    finally:
        try:
            await runner.close()
        except:
            pass

if __name__ == "__main__":
    success = asyncio.run(test_agent())
    sys.exit(0 if success else 1)

