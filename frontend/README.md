# I Got You - Frontend

Modern Next.js frontend for discovering hidden outdoor gems with AI.

## Features

- Beautiful tropical pastel green design
- Responsive mobile-first layout
- Smooth animations with Framer Motion
- Interactive Google Maps integration
- Photo galleries with lightbox
- AI-powered search and analysis
- Cost-optimized for Vercel deployment

## Tech Stack

- **Next.js 14+** with App Router
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **Framer Motion** for animations
- **React Hook Form** + **Zod** for forms
- **Google Maps API** for maps
- **yet-another-react-lightbox** for photo galleries

## Getting Started

### Prerequisites

- Node.js 18+ installed
- Google Maps API key
- Backend API running (see `/backend` directory)

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create environment variables:
```bash
cp .env.local.example .env.local
```

3. Edit `.env.local` and add your API keys:
```env
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_key_here
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Development

Run the development server:
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build

Build for production:
```bash
npm run build
```

Start production server:
```bash
npm start
```

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx              # Root layout
│   ├── page.tsx                # Homepage
│   ├── discover/
│   │   └── page.tsx           # Discovery page
│   └── api/
│       └── discover/
│           └── route.ts       # API route
├── components/
│   ├── layout/                # Header, Footer
│   ├── home/                  # Hero, HowItWorks
│   ├── discover/              # SearchForm
│   └── results/               # ResultCard, MapView, PhotoGallery
├── lib/
│   ├── api.ts                 # API client
│   ├── utils.ts               # Utilities
│   └── validations.ts         # Zod schemas
├── types/
│   └── index.ts               # TypeScript types
└── public/
    └── ...                    # Static assets (< 4KB only)
```

## Cost Optimization

This project follows Vercel cost optimization best practices:

- ✅ No large assets in `/public` (only < 4KB files)
- ✅ External images via Google Places API
- ✅ Static rendering for homepage
- ✅ Optimized image formats (AVIF, WebP)
- ✅ Proper caching strategies
- ✅ No unnecessary dynamic rendering

## Deployment

### Vercel (Recommended)

1. Push your code to GitHub
2. Import project to Vercel
3. Add environment variables in Vercel dashboard
4. Deploy!

### Environment Variables (Production)

Set these in Vercel dashboard:
- `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY`
- `NEXT_PUBLIC_API_URL` (your production API URL)

## License

MIT
