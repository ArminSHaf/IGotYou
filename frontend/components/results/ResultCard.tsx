'use client';

/**
 * ResultCard Component - Displays a Hidden Gem with All Details
 * 
 * This component renders a single hidden gem card with:
 * - Header with name, location, and rating
 * - Photo gallery
 * - Interactive map
 * - AI-generated insights
 * - Weather data and clothing recommendations (NEW!)
 * 
 * Props:
 *   gem: The hidden gem data to display
 *   index: Position in the results list (for styling/animation)
 */

import { Star, MapPin, Heart, Clock, Lightbulb, Cloud, Thermometer, Droplets, Shirt } from 'lucide-react';
import type { HiddenGem } from '@/types';
import { PhotoGallery } from './PhotoGallery';
import { MapView } from './MapView';


// ============================================================================
// COMPONENT PROPS
// ============================================================================

interface ResultCardProps {
  /** The hidden gem data to display */
  gem: HiddenGem;
  /** Position in the results list (0-indexed) */
  index: number;
}


// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

/**
 * Returns an emoji based on weather conditions
 * Makes the weather display more visually engaging
 */
function getWeatherEmoji(conditions: string, hasPrecipitation: boolean): string {
  // If there's precipitation, show rain/snow
  if (hasPrecipitation) {
    return '🌧️';
  }
  
  // Match common weather conditions to emojis
  const lowerConditions = conditions.toLowerCase();
  
  if (lowerConditions.includes('sunny') || lowerConditions.includes('clear')) {
    return '☀️';
  } else if (lowerConditions.includes('cloud') || lowerConditions.includes('overcast')) {
    return '☁️';
  } else if (lowerConditions.includes('rain') || lowerConditions.includes('shower')) {
    return '🌧️';
  } else if (lowerConditions.includes('storm') || lowerConditions.includes('thunder')) {
    return '⛈️';
  } else if (lowerConditions.includes('snow') || lowerConditions.includes('flurr')) {
    return '❄️';
  } else if (lowerConditions.includes('fog') || lowerConditions.includes('mist')) {
    return '🌫️';
  } else if (lowerConditions.includes('wind')) {
    return '💨';
  } else if (lowerConditions.includes('hot') || lowerConditions.includes('heat')) {
    return '🔥';
  }
  
  // Default to a neutral weather icon
  return '🌤️';
}


// ============================================================================
// MAIN COMPONENT
// ============================================================================

export function ResultCard({ gem, index }: ResultCardProps) {
  // Check if weather data is available and valid
  // We consider weather "available" if it has real conditions (not "unavailable" messages)
  const hasValidWeather = gem.weather && 
    gem.weather.conditions && 
    !gem.weather.conditions.toLowerCase().includes('unavailable') &&
    !gem.weather.conditions.toLowerCase().includes('location unavailable');

  return (
    <div className="bg-white rounded-lg border border-[var(--border-default)] overflow-hidden hover:border-[var(--gray-300)] hover:shadow-md transition-all">
      
      {/* ================================================================== */}
      {/* HEADER: Place Name, Location, and Rating */}
      {/* ================================================================== */}
      <div className="p-6 pb-4 border-b border-[var(--border-muted)]">
        <div className="flex items-start justify-between gap-4">
          {/* Left side: Name and Address */}
          <div className="flex-1">
            <h3 className="text-xl font-semibold text-[var(--gray-900)] mb-2">
              {gem.placeName}
            </h3>
            <div className="flex items-center gap-2 text-[var(--gray-600)]">
              <MapPin className="w-4 h-4" />
              <span className="text-sm">{gem.address}</span>
            </div>
          </div>
          
          {/* Right side: Rating Badge */}
          <div className="flex flex-col items-end gap-1">
            <div className="flex items-center gap-1 bg-[var(--accent-green)]/10 text-[var(--accent-green)] px-2.5 py-1 rounded-md border border-[var(--accent-green)]/20">
              <Star className="w-3.5 h-3.5 fill-current" />
              <span className="font-semibold text-sm">{gem.rating}</span>
            </div>
            <span className="text-xs text-[var(--gray-500)]">{gem.reviewCount} reviews</span>
          </div>
        </div>
      </div>

      {/* ================================================================== */}
      {/* PHOTO GALLERY */}
      {/* ================================================================== */}
      <div className="p-6 pb-4">
        <PhotoGallery photos={gem.photos} placeName={gem.placeName} />
      </div>

      {/* ================================================================== */}
      {/* MAP VIEW */}
      {/* ================================================================== */}
      <div className="px-6 pb-4">
        <MapView coordinates={gem.coordinates} placeName={gem.placeName} />
        <div className="mt-2 text-xs text-[var(--gray-500)]">
          Coordinates: {gem.coordinates.lat.toFixed(4)}, {gem.coordinates.lng.toFixed(4)}
        </div>
      </div>

      {/* ================================================================== */}
      {/* NEW: WEATHER & CLOTHING SECTION */}
      {/* Only displayed if we have valid weather data */}
      {/* ================================================================== */}
      {hasValidWeather && gem.weather && (
        <div className="p-6 bg-gradient-to-r from-blue-50 to-cyan-50 border-t border-[var(--border-muted)] space-y-4">
          
          {/* Section Header */}
          <h4 className="font-semibold text-[var(--gray-900)] flex items-center gap-2 text-sm">
            <Cloud className="w-4 h-4 text-blue-500" />
            Current Weather
          </h4>

          {/* Weather Data Grid */}
          <div className="grid grid-cols-3 gap-4">
            
            {/* Temperature */}
            {gem.weather.temperature !== null && (
              <div className="flex items-center gap-3 p-3 bg-white rounded-lg border border-blue-100">
                <div className="w-10 h-10 flex items-center justify-center bg-blue-100 rounded-full">
                  <Thermometer className="w-5 h-5 text-blue-600" />
                </div>
                <div>
                  <p className="text-xs text-[var(--gray-500)]">Temperature</p>
                  <p className="text-lg font-semibold text-[var(--gray-900)]">
                    {Math.round(gem.weather.temperature)}°F
                  </p>
                </div>
              </div>
            )}

            {/* Conditions */}
            <div className="flex items-center gap-3 p-3 bg-white rounded-lg border border-blue-100">
              <div className="w-10 h-10 flex items-center justify-center bg-blue-100 rounded-full text-xl">
                {getWeatherEmoji(gem.weather.conditions, gem.weather.hasPrecipitation)}
              </div>
              <div>
                <p className="text-xs text-[var(--gray-500)]">Conditions</p>
                <p className="text-sm font-medium text-[var(--gray-900)]">
                  {gem.weather.conditions}
                </p>
              </div>
            </div>

            {/* Humidity */}
            {gem.weather.humidity !== null && (
              <div className="flex items-center gap-3 p-3 bg-white rounded-lg border border-blue-100">
                <div className="w-10 h-10 flex items-center justify-center bg-blue-100 rounded-full">
                  <Droplets className="w-5 h-5 text-blue-600" />
                </div>
                <div>
                  <p className="text-xs text-[var(--gray-500)]">Humidity</p>
                  <p className="text-lg font-semibold text-[var(--gray-900)]">
                    {gem.weather.humidity}%
                  </p>
                </div>
              </div>
            )}
          </div>

          {/* Clothing Recommendation */}
          {gem.analysis.clothingRecommendation && (
            <div className="p-4 bg-amber-50 rounded-lg border border-amber-200">
              <div className="flex gap-3">
                <div className="flex-shrink-0 w-8 h-8 flex items-center justify-center bg-amber-100 rounded-full">
                  <Shirt className="w-4 h-4 text-amber-700" />
                </div>
                <div>
                  <h5 className="font-medium text-amber-900 mb-1 text-sm">
                    What to Wear
                  </h5>
                  <p className="text-sm text-amber-800">
                    {gem.analysis.clothingRecommendation}
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* ================================================================== */}
      {/* AI ANALYSIS / INSIGHTS SECTION */}
      {/* ================================================================== */}
      <div className="p-6 bg-[var(--gray-50)] border-t border-[var(--border-muted)] space-y-4">
        
        {/* Section Header */}
        <h4 className="font-semibold text-[var(--gray-900)] flex items-center gap-2 text-sm">
          <Heart className="w-4 h-4 text-[var(--gray-700)]" />
          AI Insights
        </h4>

        <div className="space-y-3">
          
          {/* Why It's Special */}
          <div className="flex gap-3">
            <div className="flex-shrink-0 w-6 h-6 rounded bg-white border border-[var(--border-default)] flex items-center justify-center">
              <Heart className="w-3.5 h-3.5 text-[var(--gray-600)]" />
            </div>
            <div>
              <p className="text-xs font-semibold text-[var(--gray-700)] mb-1">
                Why it&apos;s special
              </p>
              <p className="text-sm text-[var(--gray-600)]">{gem.analysis.whySpecial}</p>
            </div>
          </div>

          {/* Best Time to Visit */}
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

          {/* Insider Tip */}
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
