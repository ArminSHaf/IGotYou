'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { SearchForm } from '@/components/discover/SearchForm';
import { ResultCard } from '@/components/results/ResultCard';
import { BackendStatusBanner } from '@/components/BackendStatusBanner';
import { ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import type { HiddenGem } from '@/types';

export default function DiscoverPage() {
  const [results, setResults] = useState<HiddenGem[] | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (query: string) => {
    setIsLoading(true);
    setError(null);
    setResults(null);

    console.log('[Frontend] Starting search with query:', query);

    try {
      const response = await fetch('/api/discover', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ searchQuery: query }),
      });

      console.log('[Frontend] Response status:', response.status);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error('[Frontend] Error response:', errorData);

        // Show more detailed error message
        const errorMessage = errorData.detail || errorData.error || 'Failed to fetch results';
        const hint = errorData.hint ? `\n\n${errorData.hint}` : '';
        throw new Error(errorMessage + hint);
      }

      const data = await response.json();
      console.log('[Frontend] Received data:', data);
      setResults(data.gems);
    } catch (err) {
      console.error('[Frontend] Search error:', err);
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-[var(--mint-cream)] to-white">
      <BackendStatusBanner />
      <div className="container mx-auto px-4 py-12">
        {/* Back button */}
        <Link
          href="/"
          className="inline-flex items-center gap-2 text-[var(--emerald-muted)] hover:text-[var(--eucalyptus)] transition-colors mb-8"
        >
          <ArrowLeft className="w-5 h-5" />
          <span className="font-medium">Back to Home</span>
        </Link>

        {/* Search section */}
        <motion.div
          className="mb-16"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="text-center mb-12">
            <h1 className="text-4xl md:text-5xl font-bold text-[var(--emerald-muted)] mb-4">
              Discover Your Next Adventure
            </h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Tell us what kind of hidden gem you're looking for, and let AI find the perfect spots for you.
            </p>
          </div>

          <SearchForm onSearch={handleSearch} isLoading={isLoading} />
        </motion.div>

        {/* Error state */}
        {error && (
          <motion.div
            className="max-w-3xl mx-auto p-6 bg-red-50 border border-red-200 rounded-2xl text-red-700"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <h3 className="font-semibold mb-2">Oops! Something went wrong</h3>
            <p>{error}</p>
          </motion.div>
        )}

        {/* Results section */}
        {results && results.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
          >
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-[var(--emerald-muted)] mb-2">
                Hidden Gems Found
              </h2>
              <p className="text-gray-600">
                We found {results.length} amazing {results.length === 1 ? 'place' : 'places'} for you
              </p>
            </div>

            <div className="grid grid-cols-1 gap-8 max-w-5xl mx-auto">
              {results.map((gem, index) => (
                <ResultCard key={index} gem={gem} index={index} />
              ))}
            </div>

            {/* Search again button */}
            <div className="text-center mt-12">
              <button
                onClick={() => {
                  setResults(null);
                  window.scrollTo({ top: 0, behavior: 'smooth' });
                }}
                className="px-8 py-4 rounded-full border-2 border-[var(--emerald-muted)] text-[var(--emerald-muted)] font-semibold hover:bg-[var(--emerald-muted)] hover:text-white transition-all"
              >
                Search Again
              </button>
            </div>
          </motion.div>
        )}

        {/* Empty state */}
        {results && results.length === 0 && (
          <motion.div
            className="max-w-3xl mx-auto text-center p-12 bg-white rounded-2xl border border-[var(--emerald-muted)]/20"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <h3 className="text-2xl font-bold text-[var(--emerald-muted)] mb-4">
              No hidden gems found
            </h3>
            <p className="text-gray-600 mb-6">
              Try adjusting your search query or being more specific about the location and activity type.
            </p>
            <button
              onClick={() => {
                setResults(null);
                window.scrollTo({ top: 0, behavior: 'smooth' });
              }}
              className="px-8 py-3 rounded-full bg-gradient-to-r from-[var(--eucalyptus)] to-[var(--forest-light)] text-white font-semibold hover:shadow-lg transition-all"
            >
              Try Another Search
            </button>
          </motion.div>
        )}
      </div>
    </div>
  );
}
