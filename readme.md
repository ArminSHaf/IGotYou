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

The system combines Google Places API for structured data, **Gemini 2.5 Flash Lite** for intelligent analysis, and the **mcp_weather_server** (free open-source) for weather forecasts. After a spot is selected, the agent retrieves weather data for the upcoming days and determines the **best time window (“sweet spot”) for the user’s specific activity** based on conditions.

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
Step 4: Agent analyzes top reviews using Gemini 2.5 Flash Lite
Step 5: Agent retrieves weather forecast via mcp_weather_server
Step 6: Agent determines the sweet spot for the activity
Step 7: Agent returns formatted recommendations

```

### Key Differentiator

Most search tools rank by popularity.  
**I GOT YOU ranks by "hiddenness" and quality — and adds weather-optimized timing.**

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
- **mcp_weather_server** — free open-source weather data provider  

**Processing Steps**
1. Query interpretation  
2. API search  
3. Filtering for “less crowded but high quality”  
4. Review analysis  
5. Weather analysis  
6. Recommendation generation  

### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Language Model | **Gemini 2.5 Flash Lite** | Query and review analysis |
| Places Data | Google Places API | Places, ratings, reviews |
| Weather Data | **mcp_weather_server** | Weather forecasts |
| Environment | any IDE able to run Python | Platform requirement |
| Language | Python | Implementation |

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
Top 5 reviews → Gemini 2.5 Flash Lite → 3-sentence structured insight:

1. Why the spot is good  
2. Best time (from reviews) to avoid crowds  
3. Insider tip  

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
