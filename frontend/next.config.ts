import type { NextConfig } from "next";
import { config } from 'dotenv';
import { resolve } from 'path';

// Load environment variables from the root .env file (parent directory)
// This ensures Next.js can access the .env file located in the project root
// rather than looking for it in the frontend directory
config({ path: resolve(__dirname, '../.env') });

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'maps.googleapis.com',
        pathname: '/maps/api/place/photo/**',
      },
      {
        protocol: 'https',
        hostname: 'lh3.googleusercontent.com',
        pathname: '/**',
      },
      {
        protocol: 'https',
        hostname: 'images.unsplash.com',
        pathname: '/**',
      },
    ],
    formats: ['image/avif', 'image/webp'],
  },
};

export default nextConfig;
