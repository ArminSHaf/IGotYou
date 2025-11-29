# I GOT YOU - Hidden Gems Discovery Agent

**Project**: Kaggle Agents Intensive Capstone  
**Version**: 1.1  
**Date**: November 29, 2025  
**Contributors**: Alex Gutierrez, Armin Shafiei  
**Timeline**: 2 weeks development

---

![thumbnail](images/Gemini_Generated_Image_hf3kd3hf3kd3hf3k.png)

## Executive Summary

I GOT YOU is an AI agent that helps travelers discover quiet, lesser-known outdoor destinations. It solves a specific problem: popular travel tools like Google Maps prioritize highly-reviewed locations, causing crowded tourist spots to dominate results. This agent does the opposite by identifying places with **fewer reviews (less crowded spots)** but high-quality ratings, then using AI to analyze why locals love these places.

The system combines Google Places API and TripAdvisor API for structured data and reviews, **Gemini 2.5 Flash Lite** for intelligent analysis, and the **mcp_weather_server** (free open-source) for weather forecasts. After a spot is selected, the agent retrieves weather data for the upcoming days and determines the **best time window ("sweet spot") for the user's specific activity** based on conditions. The result is a working agent that can find hidden gem beaches, waterfalls, hiking trails, and other outdoor locations based on what the user is looking for.

---

## Problem Statement

### The Core Issue

Travelers searching for outdoor destinations face two major problems:

1. **Highly-reviewed spots dominate search results**, burying quieter and more authentic locations.
2. **Hidden gems are hard to find**, especially if the user doesn’t know their exact names.

### Who This Affects

Travelers seeking authentic, serene, local outdoor experiences who want alternatives to crowded attractions.

---

## Solution Overview

### What the Agent Does

The agent takes a natural-language query such as *“quiet surf spot in Bali for beginners”* and returns 2–3 recommendations for places that have:

- **Fewer reviews (less crowded spots)** —  generally lower review volume  AKA less crowded spots
- At least **3.5 star rating**  
- AI-generated insights on *why* the spot is good  
- **Weather-based timing recommendations using mcp_weather_server**

### How It Works

```
Step 1: User provides a natural language query
Step 2: Agent searches Google Places API
Step 3: Agent filters for quality but lesser-known spots (low review count + high rating)
Step 4: Agent fetches additional reviews from TripAdvisor API for selected places
Step 5: Agent analyzes reviews from both sources using Gemini 2.5 Flash Lite
Step 6: Agent retrieves weather forecast via mcp_weather_server
Step 7: Agent determines the sweet spot for the activity
Step 8: Agent returns formatted recommendations
```

### Key Differentiator

Most search tools rank by popularity.  
**I GOT YOU ranks by "hiddenness" and quality — and adds weather-optimized timing.**

---

## Output Format

### What Users Receive

When the agent completes its search and analysis, users receive comprehensive information about each recommended hidden gem location. The output includes:

#### 1. Location Information
- **Place Name**: The official name of the location
- **Address**: Full address or area description
- **Coordinates**: Geographic coordinates (latitude, longitude) for precise location
- **Rating**: Star rating (e.g., 4.6 stars)
- **Review Count**: Number of reviews (e.g., 142 reviews)

#### 2. Visual Content
- **Place Photos**: High-quality photos of the location retrieved from Google Places API
  - Multiple photos showing different angles and perspectives
  - Photos help users visualize the destination before visiting
  - Images are displayed in a gallery format for easy browsing

#### 3. Interactive Google Maps Integration
- **Map Pin**: An interactive pin marker placed on Google Maps showing the exact location
- **Clickable Navigation**: Users can click/tap the pin to:
  - Open the location directly in Google Maps application
  - Get turn-by-turn directions to the destination
  - View the location in satellite or street view mode
  - Access additional Google Maps features (save, share, etc.)

#### 4. AI-Generated Analysis
- **Why It's Special**: One-sentence explanation of what makes this spot unique
- **Best Time to Visit**: Recommendation for when to visit to avoid crowds
- **Insider Tip**: Specific advice extracted from local reviews

### Output Display Format

Each recommendation is presented as a card or section containing:
```
[Place Name]
Rating: X.X stars | Reviews: XXX

[Photo Gallery - Multiple Images]

[Interactive Google Maps with Pin]
[Click to open in Google Maps]

Location: [Address]
Coordinates: [Latitude, Longitude]

Analysis:
• Why it's special: [AI-generated insight]
• Best time to visit: [Crowd avoidance tip]
• Insider tip: [Local knowledge]
```

### User Interaction Flow

1. User submits a query (e.g., "quiet surf spot in Bali")
2. Agent processes and returns 2-3 recommendations
3. For each recommendation, user sees:
   - Location details and photos
   - Interactive map with pin
4. User clicks the map pin
5. System redirects to Google Maps with the location pre-loaded
6. User can then navigate, save, or share the location

### Technical Implementation Notes

- **Photos**: Retrieved from Google Places API `photos` field, displayed using optimized image URLs
- **Map Integration**: Uses Google Maps Embed API or Google Maps JavaScript API to display interactive map
- **Navigation Link**: Generates a Google Maps deep link (e.g., `https://www.google.com/maps/search/?api=1&query=lat,lng`) that opens the location in Google Maps
- **Responsive Design**: Output format adapts to different screen sizes (desktop, tablet, mobile)

---

## Technical Architecture

### Design Philosophy

Simple, functional, and achievable in two weeks.  
One agent handles all tasks sequentially.

### System Components

**Agent Core**  
- **Gemini 2.5 Flash Lite**  
- Handles query understanding, reasoning, review analysis, and integration steps  

**Data Sources**  
- Google Places API — places & reviews  
- TripAdvisor API — additional reviews to enrich analysis
- **mcp_weather_server** — free open-source weather data provider  

**Processing Steps**
1. Query understanding and intent extraction
2. API search with relevant parameters (Google Places API)
3. Results filtering based on hidden gem criteria
4. Fetching additional reviews from TripAdvisor API for filtered places
5. Review analysis using language model (combining reviews from both sources)
6. Weather analysis via mcp_weather_server
7. Recommendation generation with weather-optimized timing
8. Output formatting and explanation generation

### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Language Model | **Gemini 2.5 Flash Lite** | Query processing and review analysis |
| Places Data | Google Places API | Place information and reviews |
| Additional Reviews | TripAdvisor API | Additional reviews from places to enrich analysis |
| Weather Data | **mcp_weather_server** | Weather forecasts |
| Environment | any IDE able to run Python | Platform requirement |
| Language | Python | Implementation language |

**What We Are Not Using**

- Vertex AI Agent Engine (too complex for timeframe)
- LangChain (adds unnecessary abstraction)
- Vector databases (not needed for this use case)
- Multi-agent orchestration (single agent is sufficient)
- Persistent memory systems (session-only is adequate)

---

## Core Features

### Feature 1: Intelligent Filtering

**Purpose:** Find truly lesser-known spots instead of tourist-packed destinations.

**Filtering Logic:**
- Spots with **lower review counts (less crowded)**  
- Minimum **3.5+ rating**  
- Minimum review count > 10 to avoid unreliable entries  

**Success Criteria:**  
Most recommendations clearly show lighter crowds (low review volume) upon verification.

---

### Feature 2: Review Analysis with AI

**Purpose:** Generate meaningful insights explaining why each spot is special.

**Implementation:**  
The agent collects reviews from both Google Places API and TripAdvisor API for each selected place, then takes the top 5-10 reviews across both sources and sends them to Gemini 2.5 Flash Lite with a structured prompt asking for:

1. Why the spot is good (one sentence)
2. Best time (from reviews) to avoid crowds (one sentence)
3. One insider tip from the reviews (one sentence)

**Rationale**:
By combining reviews from multiple sources (Google Places and TripAdvisor), the agent gets a more comprehensive view of each location. Raw review data doesn't help users make decisions. By synthesizing reviews from multiple platforms into actionable insights, the agent provides value beyond what users could get by reading reviews from a single source themselves.

---

### Feature 3: Weather-Aware Timing Optimization

**Purpose:** Determine when the user should visit the spot in the next few days.

**Implementation:**  
- Query **mcp_weather_server** for upcoming weather  
- Analyze conditions specifically for the activity (surfing, hiking, waterfalls, etc.)  
- Produce a *"sweet spot"* recommendation:  
  - best day  
  - ideal time window  
  - justification  

Examples:  
- Surfing → wave height + wind + rain  
- Hiking → precipitation + visibility + temperature  
- Waterfalls → clouds + rainfall trends  

---

## ADK Capabilities Demonstrated

### Capability 1: Tool Use
- Google Places API  
- **mcp_weather_server**  
- Demonstrates multi-tool integration  

### Capability 2: Reasoning and Planning
The agent:  
- Filters based on crowd level → quality  
- Prioritizes relevance in reviews  
- Plans weather-based recommendations  

### Capability 3: Natural Language Understanding
Gemini 2.5 Flash Lite processes user intent + reviews.

### Capability 4 (Optional): Context Management
Session-level understanding of user activity & region.

---
## Demo Scenarios

### Scenario 1: Surf Spot Discovery

**User Query**: "quiet surf spot in Bali for beginners"

**Expected Agent Behavior**:
1. Search Google Places for surf spots in Bali
2. Filter to places with less than 300 reviews
3. Prioritize results with "beginner" mentions in reviews
4. Return 2-3 recommendations with analysis

**Example Output**:
```
Hidden Gems Found:

1. Batu Bolong Beach (North Section)
   Rating: 4.6 stars, 142 reviews
   Address: Batu Bolong Beach, Canggu, Bali, Indonesia
   
   [Photo Gallery - Multiple images of the beach and surf conditions]
   
   [Interactive Google Maps with pin at location -8.6569, 115.1381]
   [Click pin to open in Google Maps →]
   
   Analysis:
   • Why it's special: This spot offers mellow waves perfect for 
     learning without the Kuta Beach crowds.
   • Best time to visit: Local surfers recommend visiting early 
     morning between 6-8 AM when it's quietest.
   • Insider tip: The north section specifically is less busy than 
     the main beach area.
   
   Coordinates: -8.6569, 115.1381
```

---

### Scenario 2: Waterfall Discovery

**User Query**: "waterfall near Reykjavik without tour buses"

**Expected Agent Behavior**:
1. Search Google Places for waterfalls near Reykjavik
2. Filter to places with less than 300 reviews
3. Look for review mentions of "quiet" or "no crowds"
4. Return 2-3 recommendations with analysis

**Example Output**:
```
Hidden Gems Found:

1. Hjálparfoss
   Rating: 4.8 stars, 89 reviews
   Address: Hjálparfoss, Iceland
   
   [Photo Gallery - Multiple images of the waterfall and surrounding area]
   
   [Interactive Google Maps with pin at location 64.2833, -19.8833]
   [Click pin to open in Google Maps →]
   
   Analysis:
   • Why it's special: This waterfall is off the main tourist route, 
     which keeps crowds minimal.
   • Best time to visit: Visit anytime as it's consistently quiet, 
     but bring your own snacks.
   • Insider tip: Reviews consistently mention the lack of facilities, 
     which means no tour bus stops.
   
   Coordinates: 64.2833, -19.8833
```

---

## Success Metrics

### Primary Success Criteria

The agent succeeds if it meets these requirements:

1. **Runs without errors**: The Kaggle notebook executes completely
2. **Meets review threshold**: At least 80% of recommendations have fewer than 300 reviews
3. **Maintains quality**: At least 90% of recommendations have 4.0+ star ratings
4. **Provides analysis**: Every recommendation includes Gemini-generated insights
5. **Demonstrates capabilities**: All 3 required ADK capabilities are clearly shown

### Evaluation Method

**Manual Verification Process**:
For each of 10-15 test queries:
1. Run the agent and capture recommendations
2. Verify each place on Google Maps
3. Check actual review counts against claimed counts
4. Read actual reviews to verify analysis accuracy
5. Document pass/fail for each criterion

**Acceptance Standard**:
If 80% of test queries produce valid results that meet all criteria, the agent is considered successful.

---

## Risk Management

### Technical Risks

**Risk: API Rate Limits**
- Impact: Agent fails if too many requests are made
- Mitigation: Test with small query sets first, add delays between requests if needed
- Backup Plan: Cache results for demo scenarios

**Risk: Inconsistent API Results**
- Impact: Same query might return different results
- Mitigation: Document that recommendations can vary based on API updates
- Backup Plan: Show that the filtering logic is sound even if specific places change

**Risk: Poor Review Analysis**
- Impact: Gemini generates unhelpful or inaccurate insights
- Mitigation: Refine prompts during development, test multiple variations
- Backup Plan: Simplify to just showing review counts and ratings

### Timeline Risks

**Risk: Development Takes Longer Than Expected**
- Impact: May not complete in 2 weeks
- Mitigation: Build minimum viable version first, add features only if time permits
- Backup Plan: Submit with basic functionality only, document what was cut

**Risk: API Access Issues**
- Impact: Cannot develop if APIs don't work
- Mitigation: Test API access on Day 1, resolve any issues immediately
- Backup Plan: Use sample data to demonstrate concept

---

## Code Structure

### File Organization

The entire implementation exists in one Kaggle Notebook with this structure:

```
Section 1: Introduction
- Problem statement
- Solution overview

Section 2: Setup
- Package installation
- API configuration
- Library imports

Section 3: Implementation
- Search function
- Filter function
- Analysis function
- Display function

Section 4: Demo Scenarios
- Surf spot demo
- Waterfall demo

Section 5: Evaluation
- Test queries
- Results verification

Section 6: Conclusion
- Summary of results
- Limitations
- Future improvements
```

### Key Functions

**find_hidden_gems(query, max_results=3)**
- Main function that orchestrates all steps
- Returns list of recommendations

**analyze_with_gemini(place_name, reviews)**
- Sends reviews to Gemini for analysis
- Returns formatted insight text

**display_recommendations(recommendations)**
- Formats output for readability
- Shows all relevant information

---

## Limitations and Future Work

### Current Limitations

1. **Geographic Coverage**: Results depend on Google Places API coverage, which varies by region
2. **Review Analysis Depth**: Only analyzes top 5 reviews per place
3. **No Temporal Data**: Cannot access current crowd levels or Popular Times
4. **Language Limitation**: Works best with English reviews
5. **Session-Only Memory**: Does not remember preferences between sessions

### Future Enhancements

**Short Term (Next 1-2 months)**:
- Add support for more activity types beyond outdoor spots
- Implement multi-hop discovery (find hidden gems near popular landmarks)
- Add simple user feedback mechanism

**Medium Term (Next 3-6 months)**:
- Build web interface for easier access
- Add user accounts to save preferences
- Implement learning from user feedback
- Expand to restaurants and cultural sites

**Long Term (6+ months)**:
- Mobile application development
- Integration with trip planning tools
- Community features where users share hidden gems
- Partnerships with local tourism boards

---

## Submission Checklist

Before submitting to Kaggle, verify:

- [ ] Notebook runs completely without errors
- [ ] All API keys use Kaggle secrets (not hardcoded)
- [ ] Code is commented and readable
- [ ] Markdown cells explain what each section does
- [ ] Demo scenarios produce reasonable results
- [ ] At least 3 ADK capabilities are clearly demonstrated
- [ ] Evaluation section shows test results
- [ ] References to ADK documentation are included
- [ ] Total execution time is under 10 minutes
- [ ] Output is well-formatted and easy to understand

---

## References

**Competition Requirements**:
- Kaggle Agents Intensive Capstone Project Guidelines
- ADK-Python Documentation
- Vertex AI Agent Documentation

**Technical Documentation**:
- Google Places API Documentation
- TripAdvisor API Documentation
- Gemini API Reference
- Python googlemaps Library Documentation

**Related Concepts**:
- ReAct Pattern (Reasoning + Acting)
- LLM-as-Judge Evaluation Methods
- Agent Tool Use Best Practices

---

## Appendix: Sample Prompts

### Search Query Variations

For surf spots:
- "quiet surf spot in [location] for beginners"
- "uncrowded beach for surfing in [location]"
- "local surf spot in [location]"

For waterfalls:
- "waterfall near [city] without tour buses"
- "hidden waterfall in [region]"
- "quiet waterfall in [location]"

For hiking:
- "intermediate hiking trail near [city] not too popular"
- "uncrowded hike in [region]"
- "local hiking trail in [location]"

### Review Analysis Prompt Template

```
Analyze these reviews for [PLACE_NAME]:

[REVIEWS_TEXT]

Provide exactly 3 sentences:
1. Why this spot is good based on reviews
2. Best time to visit to avoid crowds
3. One specific insider tip from reviews

Be concise and specific.
```
