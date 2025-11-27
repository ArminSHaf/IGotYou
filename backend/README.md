# I Got You - Backend API

FastAPI backend wrapper for the IGotYou AI agent.

## Features

- REST API interface to Python agent
- CORS support for frontend
- Request validation with Pydantic
- Async processing
- OpenAPI documentation

## Tech Stack

- **FastAPI** for API framework
- **Uvicorn** for ASGI server
- **Pydantic** for data validation
- **Google ADK** for AI agent
- **Python 3.13+**

## Getting Started

### Prerequisites

- Python 3.13+ installed
- Google API key (Gemini)
- IGotYou_Agent module in parent directory

### Installation

1. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
```bash
# Copy from parent .env or create new
cp ../.env .env
```

Make sure `.env` contains:
```env
GOOGLE_API_KEY=your_gemini_api_key
CORS_ORIGINS=http://localhost:3000,https://your-domain.vercel.app
```

### Development

Run the development server:
```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --reload --port 8000
```

API will be available at [http://localhost:8000](http://localhost:8000)

### API Documentation

Once running, visit:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## API Endpoints

### `GET /`
Health check endpoint

Response:
```json
{
  "status": "healthy",
  "service": "I Got You API",
  "version": "1.0.0"
}
```

### `POST /api/discover`
Discover hidden gems based on search query

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
      "photos": ["url1", "url2"],
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

## Development Notes

### Current Status

The `parse_agent_response()` function currently returns mock data. You need to:

1. Implement proper parsing of the agent's text response
2. Extract place names, ratings, coordinates, etc.
3. Format into structured JSON

OR

Modify the agent to return structured JSON directly instead of plain text.

### Response Parsing

The agent returns text like:
```
Hidden Gems Found:

1. Batu Bolong Beach (North Section)
   Rating: 4.6 stars, 142 reviews
   ...
```

You'll need to parse this into the structured format expected by the frontend.

## Deployment

### Railway / Fly.io (Recommended)

1. Create account on Railway or Fly.io
2. Connect your GitHub repo
3. Set environment variables
4. Deploy!

### Environment Variables (Production)

- `GOOGLE_API_KEY` - Your Gemini API key
- `CORS_ORIGINS` - Comma-separated allowed origins

## License

MIT
