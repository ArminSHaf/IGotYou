'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Search, Loader2 } from 'lucide-react';
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
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        {/* Main search input */}
        <div className="relative">
          <div
            className={cn(
              "relative rounded-md border transition-all",
              errors.query
                ? "border-red-500 bg-red-50"
                : "border-[var(--border-default)] bg-white focus-within:border-[var(--accent-blue)] focus-within:ring-2 focus-within:ring-[var(--accent-blue)]/10"
            )}
          >
            <textarea
              {...register('query')}
              placeholder="Describe your ideal hidden gem... (e.g., 'quiet surf spot in Bali for beginners')"
              rows={4}
              disabled={isLoading}
              className="w-full px-4 py-3 rounded-md resize-none focus:outline-none bg-transparent text-[var(--gray-900)] placeholder:text-[var(--gray-400)]"
            />
          </div>

          {/* Error message */}
          {errors.query && (
            <p className="mt-2 text-sm text-red-600">
              {errors.query.message}
            </p>
          )}
        </div>

        {/* Example queries */}
        <div className="space-y-2">
          <p className="text-sm font-medium text-[var(--gray-600)]">
            Try these examples:
          </p>
          <div className="flex flex-wrap gap-2">
            {exampleQueries.map((example, index) => (
              <button
                key={index}
                type="button"
                onClick={() => handleExampleClick(example)}
                disabled={isLoading}
                className={cn(
                  "px-3 py-1.5 rounded-md text-sm font-medium transition-colors",
                  selectedExample === example
                    ? "bg-[var(--accent-blue)] text-white"
                    : "bg-[var(--gray-100)] text-[var(--gray-700)] hover:bg-[var(--gray-200)]"
                )}
              >
                {example}
              </button>
            ))}
          </div>
        </div>

        {/* Submit button */}
        <button
          type="submit"
          disabled={isLoading}
          className={cn(
            "w-full py-2.5 px-4 rounded-md font-semibold transition-colors flex items-center justify-center gap-2",
            isLoading
              ? "bg-[var(--gray-400)] text-white cursor-not-allowed"
              : "bg-[var(--accent-green)] text-white hover:bg-[var(--accent-green-light)]"
          )}
        >
          {isLoading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Searching for hidden gems...
            </>
          ) : (
            <>
              <Search className="w-5 h-5" />
              Discover Hidden Gems
            </>
          )}
        </button>

        {/* Info text */}
        {isLoading && (
          <p className="text-center text-sm text-[var(--gray-600)]">
            This usually takes 15-30 seconds. We're analyzing reviews from multiple sources...
          </p>
        )}
      </form>
    </div>
  );
}
