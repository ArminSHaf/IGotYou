'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, Loader2, Sparkles } from 'lucide-react';
import { BackendStatusBanner } from '@/components/BackendStatusBanner';
import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';

interface GemPhoto {
  name: string;
  photo_urls: string[];
  address: string;
  rating: number;
  review_count: number;
}

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  photos?: GemPhoto[];
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: "👋 Hi! I'm the IGotYou Concierge. I help you discover hidden outdoor gems around the world. Tell me what kind of experience you're looking for!",
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      role: 'user',
      content: input.trim(),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Add timeout to prevent infinite loading
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 120000); // 2 minute timeout

      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage.content,
          history: messages.map(m => ({
            role: m.role,
            content: m.content
          }))
        }),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error('Failed to get response from agent');
      }

      const data = await response.json();

      if (data.response?.trim() || (data.photos && data.photos.length > 0)) {
        const assistantMessage: Message = {
          role: 'assistant',
          content: data.response,
          timestamp: new Date(),
          photos: data.photos || undefined
        };

        setMessages(prev => [...prev, assistantMessage]);
      }
    } catch (error) {
      console.error('Chat error:', error);

      let errorContent = '❌ Sorry, I encountered an error. Please try again.';
      if (error instanceof Error) {
        if (error.name === 'AbortError') {
          errorContent = '⏱️ Request timed out. The agent is taking too long to respond. Please try again.';
        } else if (error.message.includes('fetch')) {
          errorContent = '🔌 Connection error. Please check that the backend server is running.';
        }
      }

      const errorMessage: Message = {
        role: 'assistant',
        content: errorContent,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white flex flex-col">
      <BackendStatusBanner />

      {/* Header */}
      <div className="border-b border-[var(--border-default)] bg-white sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center gap-4">
            <Link
              href="/"
              className="inline-flex items-center gap-2 text-[var(--gray-700)] hover:text-[var(--gray-900)] transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              <span className="font-medium text-sm">Back to Home</span>
            </Link>
            <div className="flex-1 text-center">
              <h1 className="text-xl font-bold text-[var(--gray-900)] flex items-center justify-center gap-2">
                <Sparkles className="w-5 h-5 text-[var(--accent-green)]" />
                Chat with IGotYou Agent
              </h1>
            </div>
            <div className="w-20"></div> {/* Spacer for centering */}
          </div>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto">
        <div className="container mx-auto px-4 py-6 max-w-4xl">
          <div className="space-y-4">
            {messages
              .filter(m => m.content.trim() || (m.photos && m.photos.length > 0))
              .map((message, index, arr) => {
                const showTimestamp = 
                  index === arr.length - 1 || 
                  arr[index + 1].role !== message.role || 
                  arr[index + 1].timestamp.getTime() - message.timestamp.getTime() > 60000;

                return (
                  <div
                    key={index}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] rounded-lg px-4 py-3 ${
                        message.role === 'user'
                          ? 'bg-[var(--accent-green)] text-white'
                          : 'bg-[var(--gray-100)] text-[var(--gray-900)]'
                      }`}
                    >
                      <div className="whitespace-pre-wrap break-words">
                        {message.content}
                      </div>

                      {/* Photo Gallery - Show photos if present */}
                      {message.photos && message.photos.length > 0 && (
                        <div className="mt-4 space-y-4">
                          {message.photos.map((gem, gemIndex) => (
                            <div key={gemIndex} className="border border-[var(--border-default)] rounded-lg overflow-hidden bg-white">
                              {/* Gem Info Header */}
                              <div className="px-3 py-2 bg-[var(--gray-50)] border-b border-[var(--border-default)]">
                                <h3 className="font-semibold text-[var(--gray-900)]">{gem.name}</h3>
                                <p className="text-xs text-[var(--gray-600)] mt-0.5">{gem.address}</p>
                                <div className="flex items-center gap-2 mt-1">
                                  <span className="text-xs font-medium text-[var(--accent-green)]">
                                    ⭐ {gem.rating.toFixed(1)}
                                  </span>
                                  <span className="text-xs text-[var(--gray-500)]">
                                    ({gem.review_count} reviews)
                                  </span>
                                </div>
                              </div>

                              {/* Photo Grid */}
                              <div className="grid grid-cols-2 gap-2 p-2">
                                {gem.photo_urls.slice(0, 4).map((url, photoIndex) => (
                                  <div key={photoIndex} className="relative aspect-video overflow-hidden rounded-md">
                                    <img
                                      src={url}
                                      alt={`${gem.name} - Photo ${photoIndex + 1}`}
                                      className="w-full h-full object-cover hover:scale-105 transition-transform duration-200"
                                      onError={(e) => {
                                        // Fallback image if photo fails to load
                                        (e.target as HTMLImageElement).src = 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=400';
                                      }}
                                    />
                                  </div>
                                ))}
                              </div>

                              {/* Show count if more than 4 photos */}
                              {gem.photo_urls.length > 4 && (
                                <div className="px-3 py-2 text-xs text-[var(--gray-600)] text-center border-t border-[var(--border-default)]">
                                  +{gem.photo_urls.length - 4} more photos
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      )}

                      {showTimestamp && (
                        <div
                          className={`text-xs mt-1 ${
                            message.role === 'user'
                              ? 'text-white/70'
                              : 'text-[var(--gray-500)]'
                          }`}
                        >
                          {message.timestamp.toLocaleTimeString([], {
                            hour: '2-digit',
                            minute: '2-digit'
                          })}
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}

            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-[var(--gray-100)] rounded-lg px-4 py-3">
                  <div className="flex items-center gap-2 text-[var(--gray-600)]">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Agent is thinking...</span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>
      </div>

      {/* Input Form */}
      <div className="border-t border-[var(--border-default)] bg-white sticky bottom-0">
        <div className="container mx-auto px-4 py-4 max-w-4xl">
          <form onSubmit={handleSubmit} className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message... (e.g., 'Find me a hidden gem in Munich')"
              disabled={isLoading}
              className="flex-1 px-4 py-3 rounded-lg border border-[var(--border-default)] focus:outline-none focus:border-[var(--accent-green)] focus:ring-2 focus:ring-[var(--accent-green)]/10 disabled:bg-[var(--gray-50)] disabled:cursor-not-allowed"
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="px-6 py-3 bg-[var(--accent-green)] text-white rounded-lg font-semibold hover:bg-[var(--accent-green-light)] transition-colors disabled:bg-[var(--gray-400)] disabled:cursor-not-allowed flex items-center gap-2"
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
              Send
            </button>
          </form>

          {/* Helpful Tips */}
          <div className="mt-3 text-xs text-[var(--gray-500)] text-center">
            💡 Tip: The agent will ask clarifying questions to understand your preferences better
          </div>
        </div>
      </div>
    </div>
  );
}
