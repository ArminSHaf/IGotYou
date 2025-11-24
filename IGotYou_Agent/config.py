import os
import googlemaps
from dotenv import load_dotenv

# Load environment API keys
load_dotenv()
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API")

if not GOOGLE_API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY in .env")
if not GOOGLE_MAPS_API_KEY:
    raise ValueError(
        "GOOGLE_MAPS_API not found in .env (Maps tools will fail)")

# 2. Shared Google Maps Client
# We create one instance here to be imported by Discovery and Analysis agents.

try:
    gmaps_client = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
except Exception as e:
    gmaps_client = None
    print(f"Error initializing Google Maps client: {e}")
