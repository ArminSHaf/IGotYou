# I Got You - Frontend

Next.js 16 frontend for discovering hidden outdoor gems.

## Features

- Tropical pastel green design
- Responsive mobile-first layout
- Smooth animations with Framer Motion
- Interactive Google Maps
- Photo galleries with lightbox
- AI-powered search

## Tech Stack

- Next.js 16 with App Router
- TypeScript
- Tailwind CSS
- Framer Motion
- React Hook Form + Zod
- Google Maps API

## Quick Start

```bash
npm install
npm run dev
```

Open http://localhost:3000

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── discover/page.tsx
│   └── api/discover/route.ts
├── components/
│   ├── layout/
│   ├── home/
│   ├── discover/
│   └── results/
├── lib/
│   ├── api.ts
│   ├── utils.ts
│   └── validations.ts
└── types/index.ts
```

## Environment Variables

Uses root `.env` via symlink:
- NEXT_PUBLIC_GOOGLE_MAPS_API_KEY
- NEXT_PUBLIC_API_URL

## Commands

```bash
npm run dev      # Development
npm run build    # Production build
npm start        # Production server
npm run lint     # Linting
```
