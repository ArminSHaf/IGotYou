'use client';

import { Compass } from 'lucide-react';

export function Footer() {
  return (
    <footer className="border-t border-[var(--border-default)] bg-[var(--gray-50)]">
      <div className="container mx-auto px-4 py-10">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Brand */}
          <div className="space-y-3">
            <div className="flex items-center space-x-2">
              <Compass className="h-5 w-5 text-[var(--gray-700)]" />
              <span className="font-semibold text-base text-[var(--gray-900)]">
                I Got You
              </span>
            </div>
            <p className="text-sm text-[var(--gray-600)]">
              Discover hidden outdoor gems with fewer than 300 reviews but amazing experiences.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-semibold text-[var(--gray-900)] mb-3 text-sm">
              Quick Links
            </h3>
            <ul className="space-y-2 text-sm text-[var(--gray-600)]">
              <li>
                <a href="/#how-it-works" className="hover:text-[var(--accent-blue)] transition-colors">
                  How It Works
                </a>
              </li>
              <li>
                <a href="/discover" className="hover:text-[var(--accent-blue)] transition-colors">
                  Start Discovering
                </a>
              </li>
            </ul>
          </div>

          {/* About */}
          <div>
            <h3 className="font-semibold text-[var(--gray-900)] mb-3 text-sm">
              About
            </h3>
            <p className="text-sm text-[var(--gray-600)]">
              Built for travelers who seek authentic experiences away from the crowds.
              Powered by AI to find places that other tools miss.
            </p>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-[var(--border-muted)] text-center text-xs text-[var(--gray-500)]">
          <p>Made for adventure seekers</p>
        </div>
      </div>
    </footer>
  );
}
