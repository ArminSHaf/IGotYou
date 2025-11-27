'use client';

import Link from 'next/link';
import { Compass } from 'lucide-react';

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-[var(--emerald-muted)]/20 bg-white/80 backdrop-blur-sm">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <Link href="/" className="flex items-center space-x-2 hover:opacity-80 transition-opacity">
          <Compass className="h-6 w-6 text-[var(--eucalyptus)]" />
          <span className="font-bold text-xl text-[var(--emerald-muted)]">
            I Got You
          </span>
        </Link>

        <nav className="hidden md:flex items-center space-x-8">
          <Link
            href="/#how-it-works"
            className="text-sm font-medium text-[var(--teal-soft)] hover:text-[var(--eucalyptus)] transition-colors"
          >
            How It Works
          </Link>
          <Link
            href="/discover"
            className="px-6 py-2 rounded-full bg-gradient-to-r from-[var(--eucalyptus)] to-[var(--forest-light)] text-white font-medium hover:shadow-lg hover:scale-105 transition-all"
          >
            Start Discovering
          </Link>
        </nav>

        {/* Mobile menu button */}
        <Link
          href="/discover"
          className="md:hidden px-4 py-2 rounded-full bg-gradient-to-r from-[var(--eucalyptus)] to-[var(--forest-light)] text-white text-sm font-medium"
        >
          Discover
        </Link>
      </div>
    </header>
  );
}
