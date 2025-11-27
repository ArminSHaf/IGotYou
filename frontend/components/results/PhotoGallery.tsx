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

  if (!photos || photos.length === 0) {
    return (
      <div className="aspect-video rounded-2xl bg-gradient-to-br from-[var(--mint-cream)] to-[var(--seafoam)] flex items-center justify-center">
        <div className="text-center text-gray-500">
          <ImageIcon className="w-12 h-12 mx-auto mb-2 opacity-50" />
          <p>No photos available</p>
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
      <div className="grid grid-cols-3 gap-2 rounded-2xl overflow-hidden">
        {displayPhotos.map((photo, index) => (
          <motion.div
            key={index}
            className={`relative cursor-pointer overflow-hidden ${
              index === 0 ? 'col-span-2 row-span-2' : 'col-span-1'
            }`}
            whileHover={{ scale: 1.05 }}
            transition={{ duration: 0.3 }}
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
            <div className="absolute inset-0 bg-black/0 hover:bg-black/10 transition-colors" />
          </motion.div>
        ))}

        {photos.length > 5 && (
          <motion.div
            className="relative cursor-pointer overflow-hidden col-span-1"
            whileHover={{ scale: 1.05 }}
            transition={{ duration: 0.3 }}
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
            <div className="absolute inset-0 bg-black/60 flex items-center justify-center">
              <span className="text-white font-semibold text-lg">
                +{photos.length - 5} more
              </span>
            </div>
          </motion.div>
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
