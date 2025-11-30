'use client';

import { useState } from 'react';
import Image from 'next/image';
import { motion } from 'framer-motion';
import Lightbox from 'yet-another-react-lightbox';
import 'yet-another-react-lightbox/styles.css';
import { ImageIcon } from 'lucide-react';

interface PhotoGalleryProps {
  photos: string[];
  placeName: string;
}

export function PhotoGallery({ photos, placeName }: PhotoGalleryProps) {
  const [lightboxOpen, setLightboxOpen] = useState(false);
  const [photoIndex, setPhotoIndex] = useState(0);
  const [imageErrors, setImageErrors] = useState<Set<number>>(new Set());

  // Filter out invalid image URLs
  const validPhotos = photos.filter((photo) => {
    if (!photo) return false;

    // Allow Google Maps URLs
    if (photo.includes('maps.googleapis.com')) {
      return true;
    }

    // Only allow URLs that look like images
    return photo.startsWith('http') && (
      photo.match(/\.(jpg|jpeg|png|gif|webp|avif)$/i) ||
      photo.includes('unsplash.com') ||
      photo.includes('googleusercontent.com')
    );
  });

  // Use placeholder if no valid photos
  const displayPhotos = validPhotos.length > 0
    ? validPhotos.slice(0, 5)
    : ['https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800'];

  if (validPhotos.length === 0 && photos.length === 0) {
    return (
      <div className="aspect-video rounded-2xl bg-gradient-to-br from-[var(--mint-cream)] to-[var(--seafoam)] flex items-center justify-center">
        <div className="text-center text-gray-500">
          <ImageIcon className="w-12 h-12 mx-auto mb-2 opacity-50" />
          <p>No photos available</p>
        </div>
      </div>
    );
  }

  const handlePhotoClick = (index: number) => {
    setPhotoIndex(index);
    setLightboxOpen(true);
  };

  return (
    <>
      <div className="flex flex-col gap-4 w-full">
        {/* Main large image */}
        {displayPhotos.length > 0 && (
          <motion.div
            className="relative cursor-pointer overflow-hidden rounded-2xl aspect-video w-full border-2 border-[var(--eucalyptus)] shadow-md"
            whileHover={{ scale: 1.02 }}
            transition={{ duration: 0.3 }}
            onClick={() => handlePhotoClick(0)}
          >
            {imageErrors.has(0) ? (
              <div className="w-full h-full bg-gradient-to-br from-[var(--mint-cream)] to-[var(--seafoam)] flex items-center justify-center">
                <ImageIcon className="w-12 h-12 text-gray-400" />
              </div>
            ) : (
              <Image
                src={displayPhotos[0]}
                alt={`${placeName} - Main Photo`}
                width={800}
                height={600}
                className="object-cover w-full h-full"
                priority
                onError={() => setImageErrors((prev) => new Set(prev).add(0))}
              />
            )}
            <div className="absolute inset-0 bg-black/0 hover:bg-black/10 transition-colors" />
          </motion.div>
        )}

        {/* Thumbnails row */}
        {displayPhotos.length > 1 && (
          <div className="grid grid-cols-4 gap-2">
            {displayPhotos.slice(1, 5).map((photo, index) => (
              <motion.div
                key={index + 1}
                className="relative cursor-pointer overflow-hidden rounded-xl aspect-square border border-[var(--eucalyptus)]/50"
                whileHover={{ scale: 1.05 }}
                transition={{ duration: 0.2 }}
                onClick={() => handlePhotoClick(index + 1)}
              >
                {imageErrors.has(index + 1) ? (
                  <div className="w-full h-full bg-gradient-to-br from-[var(--mint-cream)] to-[var(--seafoam)] flex items-center justify-center">
                    <ImageIcon className="w-6 h-6 text-gray-400" />
                  </div>
                ) : (
                  <Image
                    src={photo}
                    alt={`${placeName} - Photo ${index + 2}`}
                    width={200}
                    height={200}
                    className="object-cover w-full h-full"
                    loading="lazy"
                    onError={() => setImageErrors((prev) => new Set(prev).add(index + 1))}
                  />
                )}
              </motion.div>
            ))}

            {validPhotos.length > 5 && (
              <motion.div
                className="relative cursor-pointer overflow-hidden rounded-xl aspect-square border border-[var(--eucalyptus)]/50"
                whileHover={{ scale: 1.05 }}
                transition={{ duration: 0.2 }}
                onClick={() => handlePhotoClick(5)}
              >
                {imageErrors.has(5) ? (
                  <div className="w-full h-full bg-gradient-to-br from-[var(--mint-cream)] to-[var(--seafoam)] flex items-center justify-center">
                    <ImageIcon className="w-6 h-6 text-gray-400" />
                  </div>
                ) : (
                  <Image
                    src={validPhotos[5]}
                    alt="More photos"
                    width={200}
                    height={200}
                    className="object-cover w-full h-full"
                    loading="lazy"
                    onError={() => setImageErrors((prev) => new Set(prev).add(5))}
                  />
                )}
                <div className="absolute inset-0 bg-black/60 flex items-center justify-center">
                  <span className="text-white font-semibold text-sm">
                    +{validPhotos.length - 5}
                  </span>
                </div>
              </motion.div>
            )}
          </div>
        )}
      </div>

      <Lightbox
        open={lightboxOpen}
        close={() => setLightboxOpen(false)}
        index={photoIndex}
        slides={displayPhotos.map((photo) => ({ src: photo }))}
      />
    </>
  );
}
