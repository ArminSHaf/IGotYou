import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from IGotYou_Agent import root_agent, runner
except Exception as e:
    print(f"❌ Failed to import agent: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

async def test_interaction():
    print("\n🚀 Testing Interactive Agent Workflow")
    print("="*60)

    # Step 1: Search for gems
    query = "Find me a hidden gem in Brasov"
    print(f"\n1️⃣  Sending Query: '{query}'")
    
    try:
        response1 = await runner.run_debug(query)
        print(f"✅ Response 1 received (Length: {len(str(response1))})")
        # print(f"Preview: {str(response1)[:200]}...")
    except Exception as e:
        print(f"❌ Error in Step 1: {e}")
        return

    # Step 2: Select a gem
    selection = "Tampa Mountain" # Assuming this might be found, or just testing the flow
    print(f"\n2️⃣  Sending Selection: 'I choose {selection}'")
    
    try:
        response2 = await runner.run_debug(f"I choose {selection}")
        print(f"✅ Response 2 received (Length: {len(str(response2))})")
        print(f"Response: {response2}")
    except Exception as e:
        print(f"❌ Error in Step 2: {e}")
        return

    print("\n" + "="*60)
    print("✅ Test Completed")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(test_interaction())
