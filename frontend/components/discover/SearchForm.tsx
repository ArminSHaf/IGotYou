'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { motion } from 'framer-motion';
import { Search, Loader2, Sparkles } from 'lucide-react';
import { searchSchema, type SearchFormData } from '@/lib/validations';
import { cn } from '@/lib/utils';

const exampleQueries = [
  "Quiet surf spot in Bali for beginners",
  "Waterfall near Reykjavik without tour buses",
  "Secluded beach in Croatia for families",
  "Hidden hiking trail in Swiss Alps",
];

interface SearchFormProps {
  onSearch: (query: string) => void;
  isLoading?: boolean;
}

export function SearchForm({ onSearch, isLoading = false }: SearchFormProps) {
  const [selectedExample, setSelectedExample] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
  } = useForm<SearchFormData>({
    resolver: zodResolver(searchSchema),
  });

  const onSubmit = (data: SearchFormData) => {
    onSearch(data.query);
  };

  const handleExampleClick = (example: string) => {
    setSelectedExample(example);
    setValue('query', example);
  };

  return (
    <div className="w-full max-w-3xl mx-auto">
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Main search input */}
        <div className="relative">
          <motion.div
            className={cn(
              "relative rounded-3xl border-2 transition-all",
              errors.query
                ? "border-red-400 bg-red-50/50"
                : "border-[var(--emerald-muted)]/20 bg-white hover:border-[var(--eucalyptus)]/40 focus-within:border-[var(--eucalyptus)]"
            )}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <textarea
              {...register('query')}
              placeholder="Describe your ideal hidden gem... (e.g., 'quiet surf spot in Bali for beginners')"
              rows={4}
              disabled={isLoading}
              className="w-full px-6 py-4 pr-14 rounded-3xl resize-none focus:outline-none bg-transparent text-gray-900 placeholder:text-gray-400"
            />
            <div className="absolute right-4 bottom-4">
              <Sparkles className="w-6 h-6 text-[var(--eucalyptus)]" />
            </div>
          </motion.div>

          {/* Error message */}
          {errors.query && (
            <motion.p
              className="mt-2 text-sm text-red-600 px-4"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              {errors.query.message}
            </motion.p>
          )}
        </div>

        {/* Example queries */}
        <div className="space-y-3">
          <p className="text-sm font-medium text-gray-600 px-2">
            Try these examples:
          </p>
          <div className="flex flex-wrap gap-2">
            {exampleQueries.map((example, index) => (
              <motion.button
                key={index}
                type="button"
                onClick={() => handleExampleClick(example)}
                disabled={isLoading}
                className={cn(
                  "px-4 py-2 rounded-full text-sm font-medium transition-all",
                  selectedExample === example
                    ? "bg-[var(--eucalyptus)] text-white shadow-md"
                    : "bg-[var(--seafoam)] text-[var(--emerald-muted)] hover:bg-[var(--sage)] hover:shadow-sm"
                )}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                {example}
              </motion.button>
            ))}
          </div>
        </div>

        {/* Submit button */}
        <motion.button
          type="submit"
          disabled={isLoading}
          className={cn(
            "w-full py-4 px-8 rounded-full font-semibold text-lg shadow-lg transition-all flex items-center justify-center gap-3",
            isLoading
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-gradient-to-r from-[var(--eucalyptus)] to-[var(--forest-light)] text-white hover:shadow-xl hover:scale-105"
          )}
          whileHover={!isLoading ? { scale: 1.05 } : {}}
          whileTap={!isLoading ? { scale: 0.95 } : {}}
        >
          {isLoading ? (
            <>
              <Loader2 className="w-6 h-6 animate-spin" />
              Searching for hidden gems...
            </>
          ) : (
            <>
              <Search className="w-6 h-6" />
              Discover Hidden Gems
            </>
          )}
        </motion.button>

        {/* Info text */}
        {isLoading && (
          <motion.p
            className="text-center text-sm text-gray-600"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            This usually takes 15-30 seconds. We're analyzing reviews from multiple sources...
          </motion.p>
        )}
      </form>
    </div>
  );
}
