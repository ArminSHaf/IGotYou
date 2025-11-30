'use client';

import { useEffect, useRef } from 'react';
import { importLibrary, setOptions } from '@googlemaps/js-api-loader';
import { MapPin, ExternalLink } from 'lucide-react';
import type { Coordinates } from '@/types';

interface MapViewProps {
  coordinates: Coordinates;
  placeName: string;
}

export function MapView({ coordinates, placeName }: MapViewProps) {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<google.maps.Map | null>(null);

  const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${coordinates.lat},${coordinates.lng}`;

  useEffect(() => {
    const initMap = async () => {
      try {
        if (!mapRef.current) return;

        // Set API key using the new functional API
        setOptions({
          apiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY || '',
          version: 'weekly',
        });

        // Use the new functional API to import libraries
        const { Map } = await importLibrary('maps') as google.maps.MapsLibrary;
        const { Marker } = await importLibrary('marker') as google.maps.MarkerLibrary;

        // Custom map styles (minimal grayscale theme)
        const mapStyles: google.maps.MapTypeStyle[] = [
          {
            featureType: 'all',
            elementType: 'labels.text.fill',
            stylers: [{ color: '#6e7781' }],
          },
          {
            featureType: 'all',
            elementType: 'labels.text.stroke',
            stylers: [{ color: '#ffffff' }],
          },
          {
            featureType: 'water',
            elementType: 'geometry',
            stylers: [{ color: '#f6f8fa' }],
          },
          {
            featureType: 'landscape',
            elementType: 'geometry',
            stylers: [{ color: '#ffffff' }],
          },
          {
            featureType: 'poi.park',
            elementType: 'geometry',
            stylers: [{ color: '#eaeef2' }],
          },
          {
            featureType: 'road',
            elementType: 'geometry',
            stylers: [{ color: '#d0d7de' }],
          },
        ];

        const map = new Map(mapRef.current, {
          center: coordinates,
          zoom: 14,
          styles: mapStyles,
          disableDefaultUI: false,
          zoomControl: true,
          mapTypeControl: false,
          streetViewControl: false,
          fullscreenControl: true,
          mapId: 'IGOTYOU_MAP',
        });

        // Add custom marker
        new Marker({
          position: coordinates,
          map: map,
          title: placeName,
        });

        mapInstanceRef.current = map;
      } catch (error) {
        console.error('Error loading Google Maps:', error);
      }
    };

    initMap();
  }, [coordinates, placeName]);

  return (
    <div className="space-y-2">
      <div
        ref={mapRef}
        className="w-full h-64 rounded-md overflow-hidden border border-[var(--border-default)]"
      />
      <a
        href={mapsUrl}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex items-center gap-2 px-3 py-1.5 rounded-md text-sm bg-[var(--gray-100)] text-[var(--gray-700)] font-medium hover:bg-[var(--gray-200)] transition-colors"
      >
        <MapPin className="w-3.5 h-3.5" />
        Open in Google Maps
        <ExternalLink className="w-3.5 h-3.5" />
      </a>
    </div>
  );
}
