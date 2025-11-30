"""
Google Image Search Tool

Fetches relevant images from Google Custom Search API for a given place name.
"""

import os
import requests
from typing import List, Dict, Any


def fetch_google_images(place_name: str, max_results: int = 5) -> List[str]:
    """
    Fetch image URLs from Google Custom Search API for a given place.

    Args:
        place_name: Name of the place to search images for
        max_results: Maximum number of images to return (default: 5)

    Returns:
        List[str]: List of image URLs, or empty list if error/not configured

    Example:
        >>> fetch_google_images("Yosemite Valley", max_results=5)
        ['https://...jpg', 'https://...jpg', ...]
    """
    # Get API credentials from environment
    api_key = os.environ.get("GOOGLE_API_KEY")
    cse_id = os.environ.get("GOOGLE_CSE_ID")

    # Return empty list if not configured (graceful degradation)
    if not api_key or not cse_id:
        print(f"[Google Images] API key or CSE ID not configured - skipping image search for '{place_name}'")
        return []

    try:
        # Build search query
        # We add keywords to get better outdoor/scenic images
        search_query = f"{place_name} outdoor scenic landscape"

        # Google Custom Search API endpoint
        url = "https://www.googleapis.com/customsearch/v1"

        # API parameters
        params = {
            "key": api_key,
            "cx": cse_id,
            "q": search_query,
            "searchType": "image",  # Image search
            "num": min(max_results, 10),  # Max 10 per request
            "imgSize": "large",  # Get large images
            "fileType": "jpg,png",  # Only JPG/PNG
            "safe": "active",  # Safe search
        }

        print(f"[Google Images] Searching for: '{search_query}'")

        # Make API request
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        # Extract image URLs from results
        image_urls = []
        if "items" in data:
            for item in data["items"]:
                if "link" in item:
                    image_urls.append(item["link"])

        print(f"[Google Images] Found {len(image_urls)} images for '{place_name}'")
        return image_urls[:max_results]

    except requests.exceptions.Timeout:
        print(f"[Google Images] Timeout searching for '{place_name}'")
        return []
    except requests.exceptions.RequestException as e:
        print(f"[Google Images] API error for '{place_name}': {e}")
        return []
    except Exception as e:
        print(f"[Google Images] Unexpected error for '{place_name}': {e}")
        return []


def search_google_images_tool(place_name: str) -> dict:
    """
    Agent-friendly wrapper for Google Image Search.

    This function is designed to be used as a tool by the Gemini agent.
    It returns a dict with status and image URLs.

    Args:
        place_name: Name of the place to search images for

    Returns:
        dict: {
            "status": "success" | "not_configured" | "error",
            "images": List[str],
            "count": int
        }
    """
    try:
        # Check if API is configured
        api_key = os.environ.get("GOOGLE_API_KEY")
        cse_id = os.environ.get("GOOGLE_CSE_ID")

        if not api_key or not cse_id:
            return {
                "status": "not_configured",
                "images": [],
                "count": 0,
                "message": "Google Custom Search not configured (optional feature)"
            }

        # Fetch images
        image_urls = fetch_google_images(place_name, max_results=5)

        return {
            "status": "success",
            "images": image_urls,
            "count": len(image_urls)
        }

    except Exception as e:
        return {
            "status": "error",
            "images": [],
            "count": 0,
            "message": str(e)
        }
