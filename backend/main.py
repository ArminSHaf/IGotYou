"""
FastAPI Backend Wrapper for IGotYou Agent

This file provides a REST API interface to the IGotYou Python agent.
It handles CORS, request validation, and response formatting.
"""


import re
import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
import sys
import os
from pathlib import Path

# Add parent directory to path to import IGotYou_Agent
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
# Also add IGotYou_Agent directory to path so 'config' and 'sub_Agents' imports work
sys.path.insert(0, str(project_root / "IGotYou_Agent"))


# Import the agent (must be after path setup)
from IGotYou_Agent import root_agent, runner

app = FastAPI(
    title="I Got You API",
    description="API for discovering hidden outdoor gems",
    version="1.0.0"
)

# CORS Configuration
allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic Models
class DiscoveryRequest(BaseModel):
    searchQuery: str = Field(..., min_length=10, max_length=200)


class SelectionRequest(BaseModel):
    selection: str = Field(..., min_length=1)


class Coordinates(BaseModel):
    lat: float
    lng: float


class Analysis(BaseModel):
    whySpecial: str
    bestTime: str
    insiderTip: str


class HiddenGem(BaseModel):
    placeName: str
    address: str
    coordinates: Coordinates
    rating: float
    reviewCount: int
    photos: List[str]
    analysis: Analysis


class DiscoveryResponse(BaseModel):
    gems: List[HiddenGem]
    processingTime: float
    query: str


def parse_agent_response(raw_response: str, query: str) -> dict:
    """
    Parse the agent's JSON response. The recommendation agent now returns clean JSON.
    """
    import json

    try:
        response_text = str(raw_response).strip()
        print(
            f"[Backend] Attempting to parse JSON response (length: {len(response_text)})")

        # Remove markdown code blocks if present
        json_match = re.search(
            r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
            print(f"[Backend] Found JSON in code block")
        else:
            # Look for JSON object with "gems" array
            json_match = re.search(
                r'\{\s*"gems"\s*:\s*\[.*?\]\s*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                print(f"[Backend] Found JSON with gems array")
            else:
                # Try to extract first valid JSON object
                json_str = response_text
                # Remove any leading/trailing text
                start_idx = json_str.find('{')
                if start_idx != -1:
                    json_str = json_str[start_idx:]

        # Parse the JSON
        parsed_data = json.loads(json_str)
        print(
            f"[Backend] Successfully parsed JSON. Keys: {list(parsed_data.keys())}")

        # Validate and return
        if "gems" in parsed_data and isinstance(parsed_data["gems"], list):
            gems_count = len(parsed_data["gems"])
            print(f"[Backend] Found {gems_count} gems in response")
            return parsed_data
        else:
            print(f"[Backend] No gems array found, returning empty")
            return {"gems": []}

    except json.JSONDecodeError as e:
        print(f"[Backend] JSON decode error: {e}")
        print(f"[Backend] Response preview: {response_text[:500]}...")
        return {"gems": []}
    except Exception as e:
        print(f"[Backend] Error parsing agent response: {e}")
        print(f"[Backend] Response preview: {response_text[:500]}...")
        return {"gems": []}


def transform_gem_format(gem: dict, full_response: str = "") -> dict:
    """
    Transform analysis agent's gem format to frontend's expected format.

    Analysis agent format:
    {
        "name": "...",
        "rating": ...,
        "review_count": ...,
        "address": "...",
        "map_url": "...",
        "reviews_content": "...",
        "loc": {"lat": ..., "lng": ...}  # from discovery agent (might not be present)
    }

    Frontend format:
    {
        "placeName": "...",
        "address": "...",
        "coordinates": {"lat": ..., "lng": ...},
        "rating": ...,
        "reviewCount": ...,
        "photos": [...],
        "analysis": {
            "whySpecial": "...",
            "bestTime": "...",
            "insiderTip": "..."
        }
    }
    """
    # Extract coordinates (might be in loc field, or need to extract from map_url)
    coordinates = {"lat": 0, "lng": 0}
    if "loc" in gem and gem["loc"]:
        if isinstance(gem["loc"], dict):
            coordinates = {"lat": float(gem["loc"].get(
                "lat", 0)), "lng": float(gem["loc"].get("lng", 0))}
    elif "coordinates" in gem:
        coordinates = gem["coordinates"]

    # Try to extract coordinates from map_url if available
    if coordinates["lat"] == 0 and coordinates["lng"] == 0:
        map_url = gem.get("map_url", "")
        if map_url:
            # Extract coordinates from Google Maps URL if present
            coords_match = re.search(r'[@!](-?\d+\.\d+),(-?\d+\.\d+)', map_url)
            if coords_match:
                coordinates = {"lat": float(coords_match.group(
                    1)), "lng": float(coords_match.group(2))}

    # Try to extract analysis from the full response Markdown for this specific place
    place_name = gem.get("name", gem.get("placeName", ""))
    analysis = extract_analysis_from_markdown(place_name, full_response)

    # Generate photo URL (placeholder - in production, get from Google Places photos)
    photos = []
    if gem.get("map_url"):
        photos.append(gem["map_url"])
    photos.append(
        "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800")

    return {
        "placeName": place_name or gem.get("placeName", "Unknown Place"),
        "address": gem.get("address", "Address not available"),
        "coordinates": coordinates,
        "rating": float(gem.get("rating", 0)),
        "reviewCount": int(gem.get("review_count", gem.get("reviewCount", gem.get("reviews", 0)))),
        "photos": photos,
        "analysis": analysis
    }


def extract_analysis_from_markdown(place_name: str, markdown_text: str) -> dict:
    """
    Extract analysis (whySpecial, bestTime, insiderTip) from Markdown response.
    The recommendation agent formats this in the Markdown.
    """
    analysis = {
        "whySpecial": "A hidden gem worth exploring",
        "bestTime": "Check local hours",
        "insiderTip": "Visit during off-peak hours for the best experience"
    }

    try:
        # Find the section for this specific place
        # Look for headers with the place name
        place_section_pattern = rf'###\s*\d+\.\s*{re.escape(place_name)}.*?(?=###|$)'
        place_section = re.search(
            place_section_pattern, markdown_text, re.DOTALL | re.IGNORECASE)

        if place_section:
            section_text = place_section.group(0)

            # Extract "Why it's special"
            why_match = re.search(
                r'\*\*Why it\'s a Hidden Gem:\*\*\s*(.+?)(?=\*\*|💡|📍|🗺️|$)', section_text, re.DOTALL)
            if why_match:
                analysis["whySpecial"] = why_match.group(1).strip()

            # Extract insider tip
            tip_match = re.search(
                r'💡\s*Insider Tip:\*\*\s*(.+?)(?=\*\*|📍|🗺️|$)', section_text, re.DOTALL)
            if tip_match:
                analysis["insiderTip"] = tip_match.group(1).strip()

            # Extract best time if mentioned
            time_match = re.search(
                r'(?:best time|best visit|ideal time):\s*([^\n]+)', section_text, re.IGNORECASE)
            if time_match:
                analysis["bestTime"] = time_match.group(1).strip()
    except Exception as e:
        print(f"[Backend] Could not extract analysis from Markdown: {e}")

    return analysis


def parse_markdown_response(markdown_text: str, query: str) -> dict:
    """
    Fallback parser: Extract structured data from Markdown response.
    The recommendation agent formats data as Markdown, so we extract what we can.
    """
    import json

    gems = []

    try:
        # Look for place names (usually in headers like ### 1. Place Name)
        place_matches = re.findall(r'###\s*\d+\.\s*([^\n(]+)', markdown_text)

        # Look for ratings (⭐ [Rating])
        rating_matches = re.findall(r'⭐\s*([\d.]+)', markdown_text)

        # Look for review counts (👤 [Count] reviews)
        review_matches = re.findall(r'👤\s*(\d+)\s*reviews?', markdown_text)

        # Look for addresses (📍 Location: [Address])
        address_matches = re.findall(
            r'📍\s*Location:\s*([^\n]+)', markdown_text)

        # Look for "Why it's special" sections
        why_special_matches = re.findall(
            r'\*\*Why it\'s a Hidden Gem:\*\*\s*([^\n]+(?:\n(?!\*\*|📍|🗺️|###)[^\n]+)*)', markdown_text, re.MULTILINE)

        # Look for insider tips
        tip_matches = re.findall(
            r'💡\s*Insider Tip:\*\*\s*([^\n]+(?:\n(?!\*\*|📍|🗺️|###)[^\n]+)*)', markdown_text, re.MULTILINE)

        # Extract data for each gem found
        max_gems = max(len(place_matches), len(
            address_matches), len(why_special_matches))

        for i in range(max_gems):
            place_name = place_matches[i] if i < len(
                place_matches) else f"Place {i+1}"
            rating = float(rating_matches[i]) if i < len(
                rating_matches) else 4.0
            review_count = int(review_matches[i]) if i < len(
                review_matches) else 0
            address = address_matches[i].strip() if i < len(
                address_matches) else "Address not available"
            why_special = why_special_matches[i].strip() if i < len(
                why_special_matches) else "A hidden gem worth exploring"
            tip = tip_matches[i].strip() if i < len(
                tip_matches) else "Visit during off-peak hours for the best experience"

            # Transform to match frontend format
            gem_dict = {
                "name": place_name.strip(),  # Will be transformed by transform_gem_format
                "rating": rating,
                "review_count": review_count,
                "address": address,
                "coordinates": {"lat": 0, "lng": 0},  # Would need geocoding
            }

            # Transform using the same function used for JSON gems
            transformed_gem = transform_gem_format(gem_dict, markdown_text)
            # Override analysis since we extracted it from Markdown
            transformed_gem["analysis"] = {
                "whySpecial": why_special,
                "bestTime": "Check local hours",
                "insiderTip": tip
            }

            gems.append(transformed_gem)

        if gems:
            print(f"[Backend] Extracted {len(gems)} gems from Markdown")
            return {"gems": gems}
        else:
            # Return empty if nothing found
            return {"gems": []}

    except Exception as e:
        print(f"[Backend] Error parsing Markdown: {e}")
        return {"gems": []}


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "I Got You API",
        "version": "1.0.0"
    }


@app.post("/api/discover")
async def discover_gems(request: DiscoveryRequest):
    """
    Discover hidden outdoor gems based on search query.

    Args:
        request: Discovery request with search query

    Returns:
        DiscoveryResponse with found hidden gems
    """
    print(f"\n{'='*60}")
    print(f"[Backend] Received search query: {request.searchQuery}")
    print(f"{'='*60}")

    try:
        import time
        start_time = time.time()

        print(f"[Backend] Running agent with query: {request.searchQuery}")

        # Run the agent
        response = await runner.run_debug(request.searchQuery)

        print(
            f"[Backend] Agent response received (type: {type(response)})")
        
        # Debug: Print the full response structure to understand why extraction fails
        if isinstance(response, list):
            for i, event in enumerate(reversed(response)):
                if hasattr(event, 'role') and event.role == 'model':
                    print(f"[Backend] Event {i} content: {event.content}")
                    if hasattr(event, 'content') and hasattr(event.content, 'parts'):
                        for part in event.content.parts:
                            if hasattr(part, 'text'):
                                print(f"[Backend] Part text: {part.text[:200]}...")
                    break
        response_text = ""
        try:
            # Check if response is a string (simple case)
            if isinstance(response, str):
                response_text = response
            # Check if response is a list of events (from debug or complex run)
            elif isinstance(response, list):
                for event in reversed(response):
                    # Check for text in model response
                    if hasattr(event, 'role') and event.role == 'model':
                        if hasattr(event, 'content') and hasattr(event.content, 'parts') and event.content.parts:
                            parts = event.content.parts
                            text_parts = []
                            for part in parts:
                                if hasattr(part, 'text') and part.text:
                                    text_parts.append(part.text)
                            if text_parts:
                                response_text = "".join(text_parts)
                                break
                    
                    # Check for function_response (if root agent delegated to sub-agent)
                    if hasattr(event, 'content') and hasattr(event.content, 'parts') and event.content.parts:
                        for part in event.content.parts:
                            if hasattr(part, 'function_response') and part.function_response:
                                try:
                                    # Extract result from function response
                                    res = part.function_response.response
                                    if 'result' in res:
                                        response_text = str(res['result'])
                                        print(f"[Backend] Extracted text from function_response: {response_text[:100]}...")
                                        break
                                except Exception as e:
                                    print(f"[Backend] Error extracting function response: {e}")
                        if response_text:
                            break

            # Check if response is a single Event object
            elif hasattr(response, 'content') and hasattr(response.content, 'parts') and response.content.parts:
                 parts = response.content.parts
                 text_parts = []
                 for part in parts:
                    if hasattr(part, 'text') and part.text:
                        text_parts.append(part.text)
                    # Also check function_response in single event
                    if hasattr(part, 'function_response') and part.function_response:
                         try:
                            res = part.function_response.response
                            if 'result' in res:
                                text_parts.append(str(res['result']))
                         except:
                             pass
                 if text_parts:
                    response_text = "".join(text_parts)

            # Fallback: String conversion and robust regex
            if not response_text:
                print("[Backend] No structured text found in discovery response, trying regex...")
                response_str = str(response)
                print(f"[Backend] RAW RESPONSE DUMP: {response_str[:3000]}")
                
                # Strategy 1: Look for the specific JSON structure we expect
                # The discovery agent returns {"gems": ...}
                import json
                start_marker = '{"gems":'
                start_idx = response_str.find(start_marker)
                
                if start_idx != -1:
                    print("[Backend] Found JSON start marker in discovery response")
                    candidate = response_str[start_idx:]
                    json_found = False
                    for i in range(len(candidate), 10, -1):
                        sub = candidate[:i]
                        try:
                            data = json.loads(sub)
                            if "gems" in data:
                                response_text = sub # Use the valid JSON string
                                json_found = True
                                print("[Backend] Successfully extracted JSON via brute force")
                                break
                        except:
                            pass
                
                # Strategy 2: Regex for text='...' or text="..." (Backup)
                if not response_text:
                    import re
                    # Use re.DOTALL to match newlines
                    matches = re.findall(r"text=(['\"])((?:(?!\1).|\\.)*)\1", response_str, re.DOTALL)
                    if matches:
                        response_text = matches[-1][1]
                        response_text = response_text.replace("\\'", "'").replace('\\"', '"').replace('\\n', '\n')
                
                # Strategy 3: Brute force JSON find (if regex failed or returned non-JSON)
                if not response_text or "gems" not in response_text:
                     print("[Backend] Regex failed or no gems, trying brute force JSON search...")
                     # Find the last occurrence of "gems": [
                     json_start = response_str.rfind('{"gems":')
                     if json_start == -1:
                         json_start = response_str.rfind("{'gems':")
                     
                     if json_start != -1:
                         # Try to find the matching closing brace
                         brace_count = 0
                         for i in range(json_start, len(response_str)):
                             char = response_str[i]
                             if char == '{':
                                 brace_count += 1
                             elif char == '}':
                                 brace_count -= 1
                                 if brace_count == 0:
                                     response_text = response_str[json_start:i+1]
                                     print(f"[Backend] Brute force found JSON: {response_text[:50]}...")
                                     break

                if not response_text:
                     # CRITICAL: Do NOT return the raw event dump.
                     response_text = "I couldn't find any hidden gems matching your criteria. Please try a different query."

            # Final safety check
            if "Event(" in response_text or "model_version=" in response_text:
                 # One last try to extract JSON if we have a raw dump
                 if '{"gems":' in response_text:
                     # It's ugly but maybe valid JSON is inside
                     pass 
                 else:
                     response_text = "I couldn't find any hidden gems matching your criteria. Please try a different query."

        except Exception as e:
            print(f"[Backend] Error extracting text from response: {e}")
            response_text = "Error processing response."

        print(f"[Backend] Extracted response text preview: {response_text[:200]}...")

        # Parse JSON response from recommendation agent
        parsed_data = parse_agent_response(response_text, request.searchQuery)

        # Calculate actual processing time
        processing_time = time.time() - start_time

        gems_count = len(parsed_data.get("gems", []))
        print(f"[Backend] Successfully parsed {gems_count} gems")
        print(f"[Backend] Processing time: {processing_time:.2f}s")

        # The recommendation agent now returns data in the correct format
        gems = parsed_data.get("gems", [])

        # Validate and fix coordinates
        for gem in gems:
            if "coordinates" not in gem or not gem["coordinates"]:
                gem["coordinates"] = {"lat": 0, "lng": 0}
            elif "lat" not in gem["coordinates"] or "lng" not in gem["coordinates"]:
                 gem["coordinates"] = {"lat": 0, "lng": 0}

        # Return the response with processing time and query
        return {
            "gems": gems,
            "processingTime": processing_time,
            "query": request.searchQuery
        }

    except Exception as e:
        print(f"[Backend] ERROR in discover_gems endpoint: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )


@app.post("/api/select")
async def select_gem(request: SelectionRequest):
    """
    Handle user selection of a hidden gem.
    
    Args:
        request: Selection request with the selected gem name
        
    Returns:
        The agent's advice based on the selection and weather.
    """
    print(f"\n{'='*60}")
    print(f"[Backend] Received selection: {request.selection}")
    print(f"{'='*60}")
    
    try:
        # Construct the user input for the agent
        user_input = f"I choose {request.selection}"
        
        print(f"[Backend] Sending to agent: {user_input}")
        
        # Run the agent with the selection
        # The agent should be in the state waiting for selection (Step 2 -> Step 3)
        response = await runner.run_debug(user_input)
        
        # Extract text from response
        response_text = str(response)
        try:
            if isinstance(response, list):
                for event in reversed(response):
                    # Check for text in model response
                    if hasattr(event, 'role') and event.role == 'model':
                        if hasattr(event, 'content') and hasattr(event.content, 'parts') and event.content.parts:
                            parts = event.content.parts
                            text_parts = []
                            for part in parts:
                                if hasattr(part, 'text') and part.text:
                                    text_parts.append(part.text)
                            if text_parts:
                                response_text = "".join(text_parts)
                                break
                    
                    # Check for function_response (if root agent delegated to sub-agent)
                    if hasattr(event, 'content') and hasattr(event.content, 'parts') and event.content.parts:
                        for part in event.content.parts:
                            if hasattr(part, 'function_response') and part.function_response:
                                try:
                                    # Extract result from function response
                                    res = part.function_response.response
                                    if 'result' in res:
                                        response_text = str(res['result'])
                                        break
                                except Exception as e:
                                    print(f"[Backend] Error extracting function response: {e}")
                        if response_text:
                            break
        except Exception as e:
            print(f"[Backend] Error extracting text from response: {e}")

        print(f"[Backend] Agent response received: {response_text[:200]}...")
        
        # Try to parse response_text as JSON
        advice_data = response_text
        try:
            # Clean up potential markdown code blocks
            clean_text = response_text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:]
            if clean_text.startswith("```"):
                clean_text = clean_text[3:]
            if clean_text.endswith("```"):
                clean_text = clean_text[:-3]
            clean_text = clean_text.strip()
            
            import json
            advice_data = json.loads(clean_text)
        except Exception as e:
            print(f"[Backend] Could not parse advice as JSON, returning raw text: {e}")
            # If parsing fails, we return the raw text. 
            # The frontend should handle both string and object.
        return {
            "advice": advice_data,
            "selection": request.selection
        }
        
    except Exception as e:
        print(f"[Backend] ERROR in select_gem endpoint: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error processing selection: {str(e)}"
        )


class ChatRequest(BaseModel):
    message: str


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    Handle chat messages from the user about the selected gem.
    """
    print(f"[Backend] Received chat message: {request.message}")
    try:
        # Revert to run_debug as run() caused issues. 
        # run_debug returns a list of events.
        response = await runner.run_debug(request.message)
        
        # Extract text from response
        response_text = ""
        try:
            # Check if response is a list of events
            if isinstance(response, list):
                for event in reversed(response):
                    # Check for text in model response
                    if hasattr(event, 'role') and event.role == 'model':
                        if hasattr(event, 'content') and hasattr(event.content, 'parts') and event.content.parts:
                            parts = event.content.parts
                            text_parts = []
                            for part in parts:
                                if hasattr(part, 'text') and part.text:
                                    text_parts.append(part.text)
                            if text_parts:
                                response_text = "".join(text_parts)
                                break
                    
                    # Check for function_response (if root agent delegated to sub-agent)
                    if hasattr(event, 'content') and hasattr(event.content, 'parts') and event.content.parts:
                        for part in event.content.parts:
                            if hasattr(part, 'function_response') and part.function_response:
                                try:
                                    # Extract result from function response
                                    res = part.function_response.response
                                    if 'result' in res:
                                        response_text = str(res['result'])
                                        break
                                except Exception as e:
                                    print(f"[Backend] Error extracting function response: {e}")
                        if response_text:
                            break
            
            # Fallback: String conversion and robust regex
            if not response_text:
                response_text = ""
                response_str = str(response)
                # Removed raw dump for production

                # Strategy 1: Try to find JSON directly in the string representation if it's clean
                # The agent returns {"summary": ...}
                # We search for this pattern and try to extract the valid JSON object
                import json
                start_marker = '{"summary":'
                start_idx = response_str.find(start_marker)
                
                if start_idx != -1:
                    print("[Backend] Found JSON start marker")
                    # Try to parse increasingly shorter substrings from the end
                    # This handles the trailing characters like ')}], ...'
                    candidate = response_str[start_idx:]
                    json_found = False
                    for i in range(len(candidate), 10, -1):
                        sub = candidate[:i]
                        # We need to handle escaped quotes inside the string representation if they exist
                        # But json.loads expects valid JSON. 
                        # If the string is from repr(), it might have escaped quotes like \'
                        # Let's try to unescape first if it looks like a python string dump
                        try:
                            # Try parsing as is
                            data = json.loads(sub)
                            if "summary" in data:
                                response_text = data["summary"]
                                if "outfit" in data:
                                    response_text += f"\n\nOutfit Tip: {data['outfit']}"
                                json_found = True
                                print("[Backend] Successfully extracted JSON via brute force")
                                break
                        except:
                            # Try unescaping \' to '
                            try:
                                unescaped = sub.replace("\\'", "'").replace('\\"', '"')
                                # This might break valid JSON quotes, so it's risky.
                                # Better to rely on the regex for the text content first.
                                pass
                            except:
                                pass
                    
                    if not json_found:
                         print("[Backend] Brute force JSON parse failed")

                # Strategy 2: Regex for text='...' or text="..." (Backup)
                if not response_text:
                    import re
                    # Regex to capture text content, handling escaped quotes
                    # Matches text='...' or text="..."
                    matches = re.findall(r"text=(['\"])((?:(?!\1).|\\.)*)\1", response_str)
                    if matches:
                        # matches[0] is the quote type, matches[1] is the content
                        response_text = matches[-1][1]
                        # Unescape the string
                        response_text = response_text.replace("\\'", "'").replace('\\"', '"').replace('\\n', '\n')
                        print(f"[Backend] Regex extracted text: {response_text[:50]}...")
                    else:
                        if "Event(" in response_str:
                             print(f"[Backend] Failed to parse Event: {response_str[:200]}...")
                             # Don't give up yet, try to find ANY text
                             simple_text = re.findall(r"text=(['\"])((?:(?!\1).|\\.)*)\1", response_str)
                             if simple_text:
                                 response_text = simple_text[-1][1]
                             else:
                                 # CRITICAL: Do NOT return the raw event dump.
                                 response_text = "I'm checking the details for you. Please ask me specifically about the weather or outfit advice if I missed it!"
                        else:
                            response_text = response_str

            # Final safety check: If response_text still looks like an Event dump, replace it.
            if "Event(" in response_text or "model_version=" in response_text:
                response_text = "I successfully processed your request but couldn't generate a text summary. How can I help you further?"

            # Clean up JSON if present

            # Clean up JSON if present
            clean_text = response_text.strip()
            # Handle markdown code blocks
            if "```" in clean_text:
                code_block_match = re.search(r"```(?:json)?\s*(.*?)\s*```", clean_text, re.DOTALL)
                if code_block_match:
                    clean_text = code_block_match.group(1)
            
            # Attempt to parse as JSON if it looks like JSON
            if clean_text.startswith("{") and clean_text.endswith("}"):
                try:
                    import json
                    data = json.loads(clean_text)
                    if "summary" in data:
                        response_text = data["summary"]
                        if "outfit" in data:
                            response_text += f"\n\nOutfit Tip: {data['outfit']}"
                    elif "response" in data:
                         response_text = data["response"]
                except json.JSONDecodeError:
                    pass # Not valid JSON, treat as plain text
                except Exception as e:
                    print(f"[Backend] JSON parse error: {e}")

        except Exception as e:
            print(f"[Backend] Error extracting text from response: {e}")
            response_text = "Error processing response."

        print(f"[Backend] Agent response: {response_text[:200]}...")
        return {"response": response_text}
    except Exception as e:
        print(f"[Backend] Error processing chat request: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {e}")


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🚀 Starting I Got You Backend API Server")
    print("="*60)
    print("📍 Server will run at: http://localhost:8000")
    print("📚 API Docs available at: http://localhost:8000/docs")
    print("🔄 Waiting for requests...")
    print("="*60 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
