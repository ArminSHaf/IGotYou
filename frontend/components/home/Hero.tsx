'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { Sparkles, ArrowRight } from 'lucide-react';

export function Hero() {
  return (
    <section className="relative min-h-[90vh] flex items-center justify-center overflow-hidden bg-gradient-to-br from-[var(--mint-cream)] via-[var(--seafoam)] to-[var(--sage)]/30">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <motion.div
          className="absolute top-20 left-10 w-72 h-72 bg-[var(--eucalyptus)]/20 rounded-full blur-3xl"
          animate={{
            y: [0, 30, 0],
            scale: [1, 1.1, 1],
          }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
        <motion.div
          className="absolute bottom-20 right-10 w-96 h-96 bg-[var(--sage)]/30 rounded-full blur-3xl"
          animate={{
            y: [0, -40, 0],
            scale: [1, 1.2, 1],
          }}
          transition={{
            duration: 10,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
      </div>

      <div className="container mx-auto px-4 relative z-10">
        <motion.div
          className="text-center max-w-4xl mx-auto"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          {/* Badge */}
          <motion.div
            className="inline-flex items-center gap-2 px-4 py-2 mb-6 rounded-full bg-white/80 backdrop-blur-sm border border-[var(--emerald-muted)]/20 shadow-sm"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
          >
            <Sparkles className="w-4 h-4 text-[var(--eucalyptus)]" />
            <span className="text-sm font-medium text-[var(--emerald-muted)]">
              AI-Powered Hidden Gems Discovery
            </span>
          </motion.div>

          {/* Main heading */}
          <motion.h1
            className="text-5xl md:text-7xl font-bold mb-6 text-[var(--emerald-muted)]"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            Discover Hidden
            <br />
            <span className="font-serif bg-gradient-to-r from-[var(--eucalyptus)] to-[var(--forest-light)] bg-clip-text text-transparent">
              Outdoor Gems
            </span>
          </motion.h1>

          {/* Subheading */}
          <motion.p
            className="text-xl md:text-2xl text-gray-700 mb-10 max-w-2xl mx-auto"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            Find quiet, lesser-known destinations with fewer than 300 reviews
            but amazing experiences. Skip the crowds, discover authenticity.
          </motion.p>

          {/* CTA Buttons */}
          <motion.div
            className="flex flex-col sm:flex-row gap-4 justify-center items-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7 }}
          >
            <Link
              href="/discover"
              className="group px-8 py-4 rounded-full bg-gradient-to-r from-[var(--eucalyptus)] to-[var(--forest-light)] text-white font-semibold text-lg shadow-lg hover:shadow-xl hover:scale-105 transition-all flex items-center gap-2"
            >
              Start Discovering
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
            <a
              href="#how-it-works"
              className="px-8 py-4 rounded-full border-2 border-[var(--emerald-muted)] text-[var(--emerald-muted)] font-semibold text-lg hover:bg-[var(--emerald-muted)] hover:text-white transition-all"
            >
              Learn How It Works
            </a>
          </motion.div>

          {/* Stats */}
          <motion.div
            className="mt-16 grid grid-cols-3 gap-8 max-w-2xl mx-auto"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.9 }}
          >
            <div className="text-center">
              <div className="text-3xl font-bold text-[var(--eucalyptus)]">&lt;300</div>
              <div className="text-sm text-gray-600 mt-1">Reviews</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-[var(--eucalyptus)]">4.0+</div>
              <div className="text-sm text-gray-600 mt-1">Star Rating</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-[var(--eucalyptus)]">AI</div>
              <div className="text-sm text-gray-600 mt-1">Powered</div>
            </div>
          </motion.div>
        </motion.div>
      </div>

      {/* Scroll indicator */}
      <motion.div
        className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
        animate={{ y: [0, 10, 0] }}
        transition={{ duration: 2, repeat: Infinity }}
      >
        <div className="w-6 h-10 border-2 border-[var(--emerald-muted)]/30 rounded-full p-1">
          <div className="w-1.5 h-3 bg-[var(--eucalyptus)] rounded-full mx-auto" />
        </div>
      </motion.div>
    </section>
  );
}
