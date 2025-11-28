'use client';

import { Star, MapPin, Heart, Clock, Lightbulb } from 'lucide-react';
import type { HiddenGem } from '@/types';
import { PhotoGallery } from './PhotoGallery';
import { MapView } from './MapView';

interface ResultCardProps {
  gem: HiddenGem;
  index: number;
}

export function ResultCard({ gem, index }: ResultCardProps) {
  return (
    <div className="bg-white rounded-lg border border-[var(--border-default)] overflow-hidden hover:border-[var(--gray-300)] hover:shadow-md transition-all">
      {/* Header */}
      <div className="p-6 pb-4 border-b border-[var(--border-muted)]">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1">
            <h3 className="text-xl font-semibold text-[var(--gray-900)] mb-2">
              {gem.placeName}
            </h3>
            <div className="flex items-center gap-2 text-[var(--gray-600)]">
              <MapPin className="w-4 h-4" />
              <span className="text-sm">{gem.address}</span>
            </div>
          </div>
          <div className="flex flex-col items-end gap-1">
            <div className="flex items-center gap-1 bg-[var(--accent-green)]/10 text-[var(--accent-green)] px-2.5 py-1 rounded-md border border-[var(--accent-green)]/20">
              <Star className="w-3.5 h-3.5 fill-current" />
              <span className="font-semibold text-sm">{gem.rating}</span>
            </div>
            <span className="text-xs text-[var(--gray-500)]">{gem.reviewCount} reviews</span>
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
        <div className="mt-2 text-xs text-[var(--gray-500)]">
          Coordinates: {gem.coordinates.lat.toFixed(4)}, {gem.coordinates.lng.toFixed(4)}
        </div>
      </div>

      {/* AI Analysis */}
      <div className="p-6 bg-[var(--gray-50)] border-t border-[var(--border-muted)] space-y-4">
        <h4 className="font-semibold text-[var(--gray-900)] flex items-center gap-2 text-sm">
          <Heart className="w-4 h-4 text-[var(--gray-700)]" />
          AI Insights
        </h4>

        <div className="space-y-3">
          <div className="flex gap-3">
            <div className="flex-shrink-0 w-6 h-6 rounded bg-white border border-[var(--border-default)] flex items-center justify-center">
              <Heart className="w-3.5 h-3.5 text-[var(--gray-600)]" />
            </div>
            <div>
              <p className="text-xs font-semibold text-[var(--gray-700)] mb-1">
                Why it's special
              </p>
              <p className="text-sm text-[var(--gray-600)]">{gem.analysis.whySpecial}</p>
            </div>
          </div>

          <div className="flex gap-3">
            <div className="flex-shrink-0 w-6 h-6 rounded bg-white border border-[var(--border-default)] flex items-center justify-center">
              <Clock className="w-3.5 h-3.5 text-[var(--gray-600)]" />
            </div>
            <div>
              <p className="text-xs font-semibold text-[var(--gray-700)] mb-1">
                Best time to visit
              </p>
              <p className="text-sm text-[var(--gray-600)]">{gem.analysis.bestTime}</p>
            </div>
          </div>

          <div className="flex gap-3">
            <div className="flex-shrink-0 w-6 h-6 rounded bg-white border border-[var(--border-default)] flex items-center justify-center">
              <Lightbulb className="w-3.5 h-3.5 text-[var(--gray-600)]" />
            </div>
            <div>
              <p className="text-xs font-semibold text-[var(--gray-700)] mb-1">
                Insider tip
              </p>
              <p className="text-sm text-[var(--gray-600)]">{gem.analysis.insiderTip}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
