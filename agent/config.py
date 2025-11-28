"""
Agent Configuration

Loads environment variables and initializes shared clients.
"""

import os
import googlemaps
from dotenv import load_dotenv

# Load .env from project root
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(env_path)

# Get API keys
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GOOGLE_MAPS_API_KEY = os.environ.get("NEXT_PUBLIC_GOOGLE_MAPS_API_KEY")

# Validate required keys
if not GOOGLE_API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY in .env file")

if not GOOGLE_MAPS_API_KEY:
    raise ValueError("Missing NEXT_PUBLIC_GOOGLE_MAPS_API_KEY in .env file")

# Initialize shared Google Maps client
try:
    gmaps_client = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
except Exception as e:
    gmaps_client = None
    print(f"Error initializing Google Maps client: {e}")
