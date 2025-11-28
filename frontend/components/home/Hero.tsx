'use client';

import Link from 'next/link';
import { Sparkles, ArrowRight } from 'lucide-react';

export function Hero() {
  return (
    <section className="relative py-24 md:py-32 bg-[var(--gray-50)]">
      <div className="container mx-auto px-4">
        <div className="text-center max-w-3xl mx-auto">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-3 py-1.5 mb-6 rounded-md bg-[var(--accent-blue)]/10 border border-[var(--accent-blue)]/20">
            <Sparkles className="w-4 h-4 text-[var(--accent-blue)]" />
            <span className="text-sm font-medium text-[var(--accent-blue)]">
              AI-Powered Discovery
            </span>
          </div>

          {/* Main heading */}
          <h1 className="text-4xl md:text-6xl font-bold mb-6 text-[var(--gray-900)]">
            Discover Hidden Outdoor Gems
          </h1>

          {/* Subheading */}
          <p className="text-lg md:text-xl text-[var(--gray-600)] mb-8 max-w-2xl mx-auto">
            Find quiet, lesser-known destinations with fewer than 300 reviews
            but amazing experiences. Skip the crowds, discover authenticity.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-3 justify-center items-center mb-12">
            <Link
              href="/discover"
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-md bg-[var(--accent-green)] text-white font-semibold hover:bg-[var(--accent-green-light)] transition-colors"
            >
              Start Discovering
              <ArrowRight className="w-4 h-4" />
            </Link>
            <a
              href="#how-it-works"
              className="px-5 py-2.5 rounded-md border border-[var(--border-default)] text-[var(--gray-700)] font-semibold hover:bg-[var(--hover-bg)] hover:border-[var(--gray-300)] transition-colors"
            >
              Learn How It Works
            </a>
          </div>

          {/* Stats */}
          <div className="flex justify-center gap-12 pt-8 border-t border-[var(--border-muted)]">
            <div className="text-center">
              <div className="text-2xl font-bold text-[var(--gray-900)]">&lt;300</div>
              <div className="text-sm text-[var(--gray-600)] mt-1">Reviews</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-[var(--gray-900)]">4.0+</div>
              <div className="text-sm text-[var(--gray-600)] mt-1">Star Rating</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-[var(--gray-900)]">AI</div>
              <div className="text-sm text-[var(--gray-600)] mt-1">Powered</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
