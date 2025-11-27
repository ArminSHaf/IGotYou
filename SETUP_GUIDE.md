# I Got You - Complete Setup Guide

This guide will help you set up and run the complete IGotYou application (frontend + backend).

## Project Overview

**I Got You** is an AI-powered application that helps travelers discover hidden outdoor gems - places with fewer than 300 reviews but high ratings (4.0+). The app uses Google's Gemini AI and Google Places API to find and analyze lesser-known destinations.

## Architecture

```
IGotYou/
├── frontend/          # Next.js application (port 3000)
├── backend/           # FastAPI wrapper (port 8000)
└── IGotYou_Agent/     # Python AI agent
```

## Prerequisites

Before starting, ensure you have:

- **Node.js 18+** installed ([download](https://nodejs.org/))
- **Python 3.13+** installed ([download](https://www.python.org/downloads/))
- **Google API Key** for Gemini AI (from [Google AI Studio](https://aistudio.google.com/))
- **Google Maps API Key** (from [Google Cloud Console](https://console.cloud.google.com/))

## Step 1: Clone and Navigate

```bash
cd IGotYou
```

## Step 2: Set Up Environment Variables

The project uses a **single `.env` file** at the root level for both frontend and backend. The frontend has a symlink to this file.

1. Edit the `.env` file in the root directory:
```env
# Google API Key for Gemini and Google ADK
GOOGLE_API_KEY=your_google_api_key_here

# Google Maps API Key (for frontend - Next.js public variable)
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here

# API URL (backend endpoint for frontend)
NEXT_PUBLIC_API_URL=http://localhost:8000

# Optional: CORS origins for production
CORS_ORIGINS=http://localhost:3000
```

**Note**: The `frontend/.env` is a symlink to the root `.env` file, so both frontend and backend read from the same source.

## Step 3: Install Dependencies

### Frontend Dependencies

```bash
cd frontend
npm install
```

This installs:
- Next.js, React, TypeScript
- Tailwind CSS
- Framer Motion (animations)
- React Hook Form + Zod (forms)
- Google Maps API loader
- Photo lightbox library
- And more...

### Backend Dependencies

```bash
cd ../backend
pip install -r requirements.txt
```

This installs:
- FastAPI (API framework)
- Uvicorn (ASGI server)
- Pydantic (data validation)
- Google ADK and Gemini SDK

## Step 4: Run the Application

You'll need **two terminal windows** to run both frontend and backend.

### Terminal 1: Backend API

```bash
cd backend
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

The API will be available at:
- Main API: http://localhost:8000
- Swagger docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Terminal 2: Frontend

```bash
cd frontend
npm run dev
```

You should see:
```
  ▲ Next.js 14.x
  - Local:        http://localhost:3000
```

Open http://localhost:3000 in your browser.

## Step 5: Test the Application

1. **Homepage**: You should see the beautiful tropical green hero section
2. **Click "Start Discovering"**: Navigate to the discovery page
3. **Enter a search query**: Try "quiet surf spot in Bali for beginners"
4. **Click "Discover Hidden Gems"**: The app will search (currently returns mock data)
5. **View results**: See the result cards with photos, maps, and AI insights

## Project Features

### Frontend Features
- Tropical pastel green color scheme
- Responsive design (mobile, tablet, desktop)
- Smooth animations with Framer Motion
- Interactive Google Maps
- Photo galleries with lightbox
- Example queries for inspiration
- Loading states and error handling

### Backend Features
- REST API with FastAPI
- CORS support
- Request validation
- Async processing
- OpenAPI documentation
- Integration with IGotYou agent

## Troubleshooting

### Issue: "Module not found" errors

**Solution**: Make sure you're in the correct directory and ran `npm install` or `pip install -r requirements.txt`

### Issue: Frontend can't connect to backend

**Solution**:
1. Check that backend is running on port 8000
2. Verify `NEXT_PUBLIC_API_URL` in `.env.local` is set to `http://localhost:8000`
3. Check browser console for CORS errors

### Issue: Google Maps not displaying

**Solution**:
1. Verify you have a valid Google Maps API key
2. Make sure the API key is in `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY`
3. Check that Maps JavaScript API is enabled in Google Cloud Console

### Issue: Agent returns errors

**Solution**:
1. Verify `GOOGLE_API_KEY` is set correctly in root `.env`
2. Check that Generative Language API is enabled
3. Review backend terminal for error messages

## Next Steps

### For Development

1. ✅ **Agent Integration Complete**: The backend now uses the real IGotYou agent and parses responses

2. ✅ **Google Maps Fixed**: Updated to use the new `@googlemaps/js-api-loader` functional API

3. ✅ **Mock Data Removed**: Frontend calls the real backend API

4. **Future Enhancements**:
   - Add caching for repeated queries
   - Implement rate limiting
   - Add more detailed error messages
   - Add user feedback mechanism

### For Production

1. **Deploy Backend**: Use Railway, Fly.io, or similar
2. **Deploy Frontend**: Use Vercel (recommended)
3. **Set Environment Variables**: Add API keys in production environment
4. **Configure CORS**: Update `CORS_ORIGINS` to include production URL
5. **Set Spend Limits**: Configure Vercel spending caps

## Development Commands

### Frontend

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm start            # Start production server
npm run lint         # Run ESLint
```

### Backend

```bash
python main.py                    # Start server
uvicorn main:app --reload        # Start with auto-reload
uvicorn main:app --port 8000     # Specify port
```

## File Structure Summary

### Frontend
- `app/page.tsx` - Homepage with Hero and HowItWorks
- `app/discover/page.tsx` - Search and results page
- `app/api/discover/route.ts` - API route (currently returns mock data)
- `components/` - All React components
- `lib/` - Utilities, API client, validations
- `types/` - TypeScript type definitions

### Backend
- `main.py` - FastAPI application
- `requirements.txt` - Python dependencies

## Color Palette Reference

The tropical pastel green theme uses:
- `#F0FFF4` - Mint Cream (lightest, backgrounds)
- `#D1F4E0` - Seafoam (cards, hover states)
- `#9FE2BF` - Sage (accents)
- `#6DDCA4` - Eucalyptus (primary CTAs)
- `#52C993` - Forest Light (secondary)
- `#3DB87E` - Teal Soft (text on light)
- `#2A9D6F` - Emerald Muted (headings, borders)

## Support

For issues or questions:
1. Check this guide
2. Review the README files in `frontend/` and `backend/`
3. Check the API docs at http://localhost:8000/docs
4. Review error messages in browser console and terminal

## License

MIT
