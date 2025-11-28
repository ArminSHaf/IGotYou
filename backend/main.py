"""
FastAPI Backend for IGotYou Agent

REST API interface to the IGotYou Python agent.
Handles CORS, request validation, and response formatting.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import agent package
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
import re

from agent import root_agent, runner


# FastAPI app
app = FastAPI(
    title="I Got You API",
    description="API for discovering hidden outdoor gems using AI",
    version="1.0.0"
)

# CORS config
allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class DiscoveryRequest(BaseModel):
    searchQuery: str = Field(..., min_length=10, max_length=200)


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
    Parse the agent's response into structured JSON.
    The agent returns JSON, possibly wrapped in markdown code blocks.
    """
    import json
    
    try:
        response_text = str(raw_response)
        
        # Try to extract JSON from markdown code blocks
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
        
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find raw JSON with "gems" key
            json_match = re.search(r'\{.*"gems".*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                json_str = response_text
        
        parsed_data = json.loads(json_str)
        
        if "gems" in parsed_data and isinstance(parsed_data["gems"], list):
            return parsed_data
        else:
            raise ValueError("Invalid response format: missing 'gems' array")
        
    except Exception as e:
        print(f"Error parsing agent response: {e}")
        print(f"Raw response: {raw_response[:500]}...")
        
        # Fallback error response
        return {
            "gems": [{
                "placeName": "Unable to parse results",
                "address": "Please try a different search query",
                "coordinates": {"lat": 0, "lng": 0},
                "rating": 0,
                "reviewCount": 0,
                "photos": ["https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800"],
                "analysis": {
                    "whySpecial": f"Error: {str(e)}",
                    "bestTime": "N/A",
                    "insiderTip": "Try rephrasing your search query"
                }
            }]
        }


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "healthy", "service": "I Got You API", "version": "1.0.0"}


@app.post("/api/discover")
async def discover_gems(request: DiscoveryRequest):
    """
    Discover hidden outdoor gems based on search query.
    Runs the full agent pipeline: Discovery -> Analysis -> Recommendation
    """
    print(f"\n{'='*60}")
    print(f"Received search query: {request.searchQuery}")
    print(f"{'='*60}")
    
    try:
        import time
        start_time = time.time()
        
        print("Running agent...")
        response = await runner.run_debug(request.searchQuery)
        
        print(f"Agent response received (length: {len(str(response))})")
        
        parsed_data = parse_agent_response(str(response), request.searchQuery)
        processing_time = time.time() - start_time
        
        print(f"Parsed {len(parsed_data['gems'])} gems in {processing_time:.2f}s")
        
        return {
            "gems": parsed_data["gems"],
            "processingTime": processing_time,
            "query": request.searchQuery
        }
        
    except Exception as e:
        print(f"Error in discover_gems: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown."""
    try:
        await runner.close()
    except:
        pass


if __name__ == "__main__":
    import uvicorn
    print("\nStarting I Got You Backend API Server")
    print("Server: http://localhost:8000")
    print("Docs:   http://localhost:8000/docs\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
