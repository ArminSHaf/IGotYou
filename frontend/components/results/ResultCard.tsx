'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Star, MapPin, Heart, Clock, Lightbulb, Check, Loader2 } from 'lucide-react';
import type { HiddenGem } from '@/types';
import { PhotoGallery } from './PhotoGallery';
import { MapView } from './MapView';
import { ChatInterface } from './ChatInterface';

interface ResultCardProps {
  gem: HiddenGem;
  index: number;
}

export function ResultCard({ gem, index }: ResultCardProps) {
  const [isSelected, setIsSelected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [advice, setAdvice] = useState<string | object | null>(null);

  const handleSelect = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('/api/select', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ selection: gem.placeName }),
      });

      if (!response.ok) {
        throw new Error('Failed to select gem');
      }

      const data = await response.json();
      setAdvice(data.advice);
      setIsSelected(true);
    } catch (error) {
      console.error('Selection error:', error);
      // Optional: Handle error state
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <motion.div
      className="bg-white rounded-3xl border border-[var(--emerald-muted)]/20 overflow-hidden shadow-lg hover:shadow-xl transition-all"
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: index * 0.2 }}
      whileHover={{ y: -8 }}
    >
      {/* Header */}
      <div className="p-6 pb-4 border-b border-[var(--emerald-muted)]/10">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1">
            <h3 className="text-2xl font-bold text-[var(--emerald-muted)] mb-2">
              {gem.placeName}
            </h3>
            <div className="flex items-center gap-2 text-gray-600">
              <MapPin className="w-4 h-4" />
              <span className="text-sm">{gem.address}</span>
            </div>
          </div>
          <div className="flex flex-col items-end gap-1">
            <div className="flex items-center gap-1 bg-gradient-to-r from-[var(--eucalyptus)] to-[var(--forest-light)] text-white px-3 py-1 rounded-full">
              <Star className="w-4 h-4 fill-current" />
              <span className="font-semibold">{gem.rating}</span>
            </div>
            <span className="text-xs text-gray-500">{gem.reviewCount} reviews</span>
          </div>
        </div>
      </div>

      {/* Photo Gallery */}
      <div className="p-6 pb-4">
        <PhotoGallery photos={gem.photos} placeName={gem.placeName} />
      </div>

      {/* Map */}
      <div className="px-6 pb-4">
        <MapView coordinates={gem.coordinates} placeName={gem.placeName} />
        <div className="mt-2 text-xs text-gray-500">
          Coordinates: {gem.coordinates.lat.toFixed(4)}, {gem.coordinates.lng.toFixed(4)}
        </div>
      </div>

      {/* AI Analysis */}
      <div className="p-6 bg-gradient-to-br from-[var(--mint-cream)] to-[var(--seafoam)]/50 space-y-4">
        <h4 className="font-semibold text-[var(--emerald-muted)] flex items-center gap-2">
          <Heart className="w-5 h-5 text-[var(--eucalyptus)]" />
          AI Insights
        </h4>

        <div className="space-y-3">
          <div className="flex gap-3">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-white/80 flex items-center justify-center">
              <Heart className="w-4 h-4 text-[var(--eucalyptus)]" />
            </div>
            <div>
              <p className="text-sm font-medium text-[var(--emerald-muted)] mb-1">
                Why it's special
              </p>
              <p className="text-sm text-gray-700">{gem.analysis.whySpecial}</p>
            </div>
          </div>

          <div className="flex gap-3">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-white/80 flex items-center justify-center">
              <Clock className="w-4 h-4 text-[var(--eucalyptus)]" />
            </div>
            <div>
              <p className="text-sm font-medium text-[var(--emerald-muted)] mb-1">
                Best time to visit
              </p>
              <p className="text-sm text-gray-700">{gem.analysis.bestTime}</p>
            </div>
          </div>

          <div className="flex gap-3">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-white/80 flex items-center justify-center">
              <Lightbulb className="w-4 h-4 text-[var(--eucalyptus)]" />
            </div>
            <div>
              <p className="text-sm font-medium text-[var(--emerald-muted)] mb-1">
                Insider tip
              </p>
              <p className="text-sm text-gray-700">{gem.analysis.insiderTip}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Selection Section */}
      <div className="p-6 pt-0 bg-gradient-to-br from-[var(--mint-cream)] to-[var(--seafoam)]/50">
        {!advice ? (
          <button
            onClick={handleSelect}
            disabled={isLoading}
            className="w-full py-3 px-6 rounded-xl bg-green-600 hover:bg-green-700 text-white font-semibold shadow-lg hover:shadow-xl transition-all flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Checking Weather...
              </>
            ) : (
              <>
                <Check className="w-5 h-5" />
                Select this Gem
              </>
            )}
          </button>
        ) : (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
          >
            <ChatInterface initialAdvice={advice} placeName={gem.placeName} />
          </motion.div>
        )}
      </div>
    </motion.div>
  );
}
