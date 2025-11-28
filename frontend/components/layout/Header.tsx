'use client';

import Link from 'next/link';
import { Compass } from 'lucide-react';

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-[var(--border-default)] bg-white">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <Link href="/" className="flex items-center space-x-2 hover:opacity-70 transition-opacity">
          <Compass className="h-5 w-5 text-[var(--gray-900)]" />
          <span className="font-semibold text-base text-[var(--gray-900)]">
            I Got You
          </span>
        </Link>

        <nav className="hidden md:flex items-center space-x-4">
          <Link
            href="/#how-it-works"
            className="text-sm font-medium text-[var(--gray-700)] hover:text-[var(--gray-900)] transition-colors px-3 py-2"
          >
            How It Works
          </Link>
          <Link
            href="/discover"
            className="px-4 py-1.5 rounded-md bg-[var(--accent-green)] text-white text-sm font-medium hover:bg-[var(--accent-green-light)] transition-colors"
          >
            Start Discovering
          </Link>
        </nav>

        {/* Mobile menu button */}
        <Link
          href="/discover"
          className="md:hidden px-3 py-1.5 rounded-md bg-[var(--accent-green)] text-white text-sm font-medium hover:bg-[var(--accent-green-light)] transition-colors"
        >
          Discover
        </Link>
      </div>
    </header>
  );
}
