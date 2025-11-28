# I Got You - Backend API

FastAPI backend that wraps the IGotYou AI agent.

## Quick Start

```bash
cd backend
python main.py
```

Server runs at http://localhost:8000

## API Endpoints

### GET /
Health check.

### POST /api/discover
Discover hidden outdoor gems.

Request:
```json
{
  "searchQuery": "quiet surf spot in Bali for beginners"
}
```

Response:
```json
{
  "gems": [
    {
      "placeName": "Batu Bolong Beach",
      "address": "Canggu, Bali, Indonesia",
      "coordinates": { "lat": -8.6569, "lng": 115.1381 },
      "rating": 4.6,
      "reviewCount": 142,
      "photos": ["url"],
      "analysis": {
        "whySpecial": "...",
        "bestTime": "...",
        "insiderTip": "..."
      }
    }
  ],
  "processingTime": 15.2,
  "query": "quiet surf spot in Bali for beginners"
}
```

## Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables

From root `.env`:
- GOOGLE_API_KEY - Gemini API key
- CORS_ORIGINS - Allowed frontend origins
