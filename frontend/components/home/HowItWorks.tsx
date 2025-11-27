'use client';

import { motion } from 'framer-motion';
import { Search, Sparkles, MapPin, Camera } from 'lucide-react';

const steps = [
  {
    icon: Search,
    title: "Tell Us What You're Looking For",
    description: "Describe your ideal destination in natural language. Be specific about activities, location, and preferences.",
  },
  {
    icon: Sparkles,
    title: "AI Finds Hidden Gems",
    description: "Our AI searches for places with fewer than 300 reviews and at least 4.0 stars - truly hidden quality spots.",
  },
  {
    icon: Camera,
    title: "Get Insights from Reviews",
    description: "We analyze real reviews to explain why each place is special, best times to visit, and insider tips.",
  },
  {
    icon: MapPin,
    title: "Explore Photos & Maps",
    description: "View photo galleries and interactive Google Maps. Click to get directions and plan your visit.",
  },
];

export function HowItWorks() {
  return (
    <section id="how-it-works" className="py-24 bg-white">
      <div className="container mx-auto px-4">
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="text-4xl md:text-5xl font-bold text-[var(--emerald-muted)] mb-4">
            How It Works
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Four simple steps to discover your next adventure
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {steps.map((step, index) => (
            <motion.div
              key={index}
              className="relative"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
            >
              <div className="bg-gradient-to-br from-[var(--mint-cream)] to-[var(--seafoam)] rounded-3xl p-8 h-full border border-[var(--emerald-muted)]/10 hover:border-[var(--eucalyptus)]/30 transition-all hover:shadow-lg">
                {/* Step number */}
                <div className="absolute -top-4 -left-4 w-12 h-12 rounded-full bg-gradient-to-br from-[var(--eucalyptus)] to-[var(--forest-light)] text-white font-bold text-xl flex items-center justify-center shadow-lg">
                  {index + 1}
                </div>

                {/* Icon */}
                <div className="mb-6 inline-flex p-4 rounded-2xl bg-white/80 backdrop-blur-sm shadow-sm">
                  <step.icon className="w-8 h-8 text-[var(--eucalyptus)]" />
                </div>

                {/* Content */}
                <h3 className="text-xl font-bold text-[var(--emerald-muted)] mb-3">
                  {step.title}
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  {step.description}
                </p>
              </div>

              {/* Connector line (not on last item) */}
              {index < steps.length - 1 && (
                <div className="hidden lg:block absolute top-1/2 -right-4 w-8 h-0.5 bg-gradient-to-r from-[var(--eucalyptus)] to-[var(--forest-light)]/30" />
              )}
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
