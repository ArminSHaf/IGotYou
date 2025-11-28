'use client';

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
    <section id="how-it-works" className="py-16 md:py-24 bg-white">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-[var(--gray-900)] mb-3">
            How It Works
          </h2>
          <p className="text-lg text-[var(--gray-600)] max-w-2xl mx-auto">
            Four simple steps to discover your next adventure
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {steps.map((step, index) => (
            <div
              key={index}
              className="relative bg-white rounded-lg border border-[var(--border-default)] p-6 hover:border-[var(--gray-300)] hover:shadow-md transition-all"
            >
              {/* Step number */}
              <div className="inline-flex items-center justify-center w-8 h-8 rounded-full bg-[var(--gray-100)] text-[var(--gray-700)] font-semibold text-sm mb-4">
                {index + 1}
              </div>

              {/* Icon */}
              <div className="mb-4">
                <step.icon className="w-6 h-6 text-[var(--gray-700)]" />
              </div>

              {/* Content */}
              <h3 className="text-base font-semibold text-[var(--gray-900)] mb-2">
                {step.title}
              </h3>
              <p className="text-sm text-[var(--gray-600)] leading-relaxed">
                {step.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
