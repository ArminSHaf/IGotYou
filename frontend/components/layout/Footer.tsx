'use client';

import { Compass, Heart } from 'lucide-react';

export function Footer() {
  return (
    <footer className="border-t border-[var(--emerald-muted)]/20 bg-gradient-to-b from-white to-[var(--mint-cream)]">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Brand */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <Compass className="h-6 w-6 text-[var(--eucalyptus)]" />
              <span className="font-bold text-xl text-[var(--emerald-muted)]">
                I Got You
              </span>
            </div>
            <p className="text-sm text-gray-600">
              Discover hidden outdoor gems with fewer than 300 reviews but amazing experiences.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-semibold text-[var(--emerald-muted)] mb-4">
              Quick Links
            </h3>
            <ul className="space-y-2 text-sm text-gray-600">
              <li>
                <a href="/#how-it-works" className="hover:text-[var(--eucalyptus)] transition-colors">
                  How It Works
                </a>
              </li>
              <li>
                <a href="/discover" className="hover:text-[var(--eucalyptus)] transition-colors">
                  Start Discovering
                </a>
              </li>
            </ul>
          </div>

          {/* About */}
          <div>
            <h3 className="font-semibold text-[var(--emerald-muted)] mb-4">
              About
            </h3>
            <p className="text-sm text-gray-600">
              Built for travelers who seek authentic experiences away from the crowds.
              Powered by AI to find places that other tools miss.
            </p>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-[var(--emerald-muted)]/20 text-center text-sm text-gray-600">
          <p className="flex items-center justify-center gap-1">
            Made with <Heart className="h-4 w-4 text-[var(--eucalyptus)] fill-current" /> for adventure seekers
          </p>
        </div>
      </div>
    </footer>
  );
}
