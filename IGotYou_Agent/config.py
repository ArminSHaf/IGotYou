import os
import googlemaps
from dotenv import load_dotenv
from pathlib import Path

# Load environment API keys
# Look for .env file in the root directory (parent of IGotYou_Agent)
root_dir = Path(__file__).parent.parent
env_path = root_dir / ".env"
load_dotenv(env_path)

# Also try loading from IGotYou_Agent directory as fallback
if not os.path.exists(env_path):
    env_path_fallback = Path(__file__).parent / ".env"
    load_dotenv(env_path_fallback)

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API")

if not GOOGLE_API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY in .env")
if not GOOGLE_MAPS_API_KEY:
    raise ValueError(
        "GOOGLE_MAPS_API not found in .env (Maps tools will fail)")

# Set as environment variable for Google ADK to pick up automatically
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# 2. Shared Google Maps Client
# We create one instance here to be imported by Discovery and Analysis agents.

try:
    gmaps_client = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
except Exception as e:
    gmaps_client = None
    print(f"Error initializing Google Maps client: {e}")
