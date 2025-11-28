'use client';

import { useState } from 'react';
import Image from 'next/image';
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

  if (!photos || photos.length === 0) {
    return (
      <div className="aspect-video rounded-md bg-[var(--gray-50)] border border-[var(--border-muted)] flex items-center justify-center">
        <div className="text-center text-[var(--gray-500)]">
          <ImageIcon className="w-10 h-10 mx-auto mb-2" />
          <p className="text-sm">No photos available</p>
        </div>
      </div>
    );
  }

  const displayPhotos = photos.slice(0, 5);

  const handlePhotoClick = (index: number) => {
    setPhotoIndex(index);
    setLightboxOpen(true);
  };

  return (
    <>
      <div className="grid grid-cols-3 gap-2 rounded-md overflow-hidden border border-[var(--border-default)]">
        {displayPhotos.map((photo, index) => (
          <div
            key={index}
            className={`relative cursor-pointer overflow-hidden hover:opacity-90 transition-opacity ${
              index === 0 ? 'col-span-2 row-span-2' : 'col-span-1'
            }`}
            onClick={() => handlePhotoClick(index)}
          >
            <Image
              src={photo}
              alt={`${placeName} - Photo ${index + 1}`}
              width={index === 0 ? 600 : 300}
              height={index === 0 ? 600 : 300}
              className="object-cover w-full h-full"
              loading="lazy"
            />
          </div>
        ))}

        {photos.length > 5 && (
          <div
            className="relative cursor-pointer overflow-hidden col-span-1 hover:opacity-90 transition-opacity"
            onClick={() => handlePhotoClick(5)}
          >
            <Image
              src={photos[5]}
              alt={`${placeName} - More photos`}
              width={300}
              height={300}
              className="object-cover w-full h-full"
              loading="lazy"
            />
            <div className="absolute inset-0 bg-black/70 flex items-center justify-center">
              <span className="text-white font-semibold text-sm">
                +{photos.length - 5} more
              </span>
            </div>
          </div>
        )}
      </div>

      <Lightbox
        open={lightboxOpen}
        close={() => setLightboxOpen(false)}
        index={photoIndex}
        slides={photos.map((photo) => ({ src: photo }))}
      />
    </>
  );
}
