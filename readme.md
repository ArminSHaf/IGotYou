# I GOT YOU - Hidden Gems Discovery Agent

**Project:** Kaggle Agents Intensive Capstone  
**Version:** 1.1  
**Date:** November 29, 2025  
**Contributors:** Alex Gutierrez, Armin Shafiei  
**Timeline:** 2 weeks development

---

![thumbnail](images/Gemini_Generated_Image_hf3kd3hf3kd3hf3k.png)

## Executive Summary

**I GOT YOU** is an AI agent designed to help travelers discover quiet, lesser-known outdoor destinations. It addresses a specific limitation in popular travel tools like Google Maps, which prioritize highly-reviewed locations and inadvertently direct users to crowded tourist hubs. This agent reverses that logic by identifying places with **lower review volumes (indicating fewer crowds)** that still maintain high quality ratings.

The system combines the **Google Places API** for structured data, **Gemini 2.5 Flash Lite** for intelligent analysis, and the **mcp_weather_server** (open-source) for real-time forecasting. Once a destination is selected, the agent analyzes upcoming weather conditions to recommend the **"sweet spot"**—the optimal time window for the user’s specific activity.

---

## Problem Statement

### The Core Issue
Travelers searching for outdoor destinations face two major hurdles:
1.  **Popularity Bias:** Highly-reviewed spots dominate search results, burying quieter, authentic locations.
2.  **Discovery Friction:** True "hidden gems" are difficult to find without knowing their specific names.

### Who This Affects
Travelers seeking authentic, serene, and local outdoor experiences who want alternatives to crowded mainstream attractions.

---

## Solution Overview

### What the Agent Does
The agent accepts natural-language queries (e.g., *“quiet surf spot in Bali for beginners”*) and returns 2–3 recommendations that feature:
* **Low Review Volume:** Indicates a less crowded location.
* **High Quality:** Minimum 3.5-star rating.
* **AI Insights:** Generated explanations on *why* locals love the spot.
* **Smart Timing:** Weather-based recommendations via `mcp_weather_server`.

### How It Works
1.  **User Input:** The user provides a natural language query.
2.  **Search:** The agent queries the Google Places API.
3.  **Filter:** The agent filters for quality but lesser-known spots (low review count + high rating).
4.  **Analyze:** Gemini 2.5 Flash Lite analyzes the top reviews to extract insights.
5.  **Forecast:** The agent retrieves weather data via `mcp_weather_server`.
6.  **Optimize:** The agent determines the best time window for the specific activity.
7.  **Recommend:** The agent presents the final formatted results.

### Key Differentiator
Most search tools rank by popularity. **I GOT YOU ranks by "hiddenness" and quality—then optimizes for weather.**

---

## Technical Architecture

### Design Philosophy
Simple, functional, and achievable within a two-week sprint. A single root agent orchestrates the workflow sequentially.

### System Components
* **Agent Core:**
    * **Gemini 2.5 Flash Lite:** Handles query understanding, reasoning, review analysis, and step integration.
* **Data Sources:**
    * **Google Places API:** Provides location data, ratings, and reviews.
    * **mcp_weather_server:** Provides free, open-source weather data.
* **Processing Steps:**
    1.  Query interpretation
    2.  API search
    3.  Filtering (Crowd level vs. Quality)
    4.  Review analysis
    5.  Weather analysis
    6.  Recommendation generation

### Technology Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Language Model** | Gemini 2.5 Flash Lite | Query and review analysis |
| **Places Data** | Google Places API | Places, ratings, reviews |
| **Weather Data** | mcp_weather_server | Weather forecasts |
| **Environment** | Python-compatible IDE | Platform requirement |
| **Language** | Python | Implementation |

---

## Core Features

### Feature 1: Intelligent Filtering
**Purpose:** To surface truly lesser-known spots rather than tourist traps.

**Filtering Logic:**
* **Low Review Counts:** Proxies for "less crowded."
* **Quality Threshold:** Minimum 3.5+ star rating.
* **Reliability Floor:** Minimum >10 reviews to avoid data errors.

**Success Criteria:**
Recommendations consistently show lighter crowds (verified by review volume) compared to top search results.

### Feature 2: Review Analysis with AI
**Purpose:** To generate meaningful insights that explain a spot's unique appeal.

**Implementation:**
The agent analyzes the top 5 reviews using Gemini 2.5 Flash Lite to produce a 3-part structured insight:
1.  **Why it's special**
2.  **Best time to visit** (based on user feedback)
3.  **Insider tips**

### Feature 3: Weather-Aware Timing Optimization
**Purpose:** To determine the optimal visit time over the next few days.

**Implementation:**
* Queries `mcp_weather_server` for the forecast.
* Analyzes conditions relative to the activity (e.g., Surf, Hike, Waterfall).
* Produces a **"Sweet Spot"** recommendation including the best day, ideal time window, and justification.

**Examples:**
* *Surfing:* Wave height + Wind speed + Rain
* *Hiking:* Precipitation + Visibility + Temperature
* *Waterfalls:* Cloud cover + Recent rainfall trends

---

## ADK Capabilities Demonstrated

### Capability 1: Tool Use
* Integration of Google Places API and `mcp_weather_server`.
* Demonstrates effective multi-tool chaining.

### Capability 2: Reasoning and Planning
* Filters candidates based on the trade-off between crowd level and quality.
* Prioritizes relevance within review text.
* Plans recommendations based on external weather variables.

### Capability 3: Natural Language Understanding
* Utilizes Gemini 2.5 Flash Lite to interpret user intent and synthesize unstructured review data.

### Capability 4: Context Management
* Maintains session-level understanding of the user's desired activity and target region.