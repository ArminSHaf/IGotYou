'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, User, Bot, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface Message {
    role: 'user' | 'assistant';
    content: string | object;
}

interface ChatInterfaceProps {
    initialAdvice: string | object;
    placeName: string;
}

export function ChatInterface({ initialAdvice, placeName }: ChatInterfaceProps) {
    const [messages, setMessages] = useState<Message[]>([
        { role: 'assistant', content: initialAdvice }
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

        const userMessage = input.trim();
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
        setIsLoading(true);

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMessage }),
            });

            if (!response.ok) throw new Error('Failed to send message');

            const data = await response.json();

            // Clean up response if it looks like a raw log
            let cleanResponse = data.response;
            if (cleanResponse && typeof cleanResponse === 'string' && (cleanResponse.includes('[Event(') || cleanResponse.includes('Event('))) {
                console.log('Detected raw log in response, attempting to clean...');
                // Try to extract JSON summary
                const jsonMatch = cleanResponse.match(/{"summary":\s*"(.*?)"/);
                if (jsonMatch) {
                    const startIdx = cleanResponse.indexOf('{"summary":');
                    if (startIdx !== -1) {
                        let candidate = cleanResponse.substring(startIdx);
                        for (let i = candidate.length; i > 10; i--) {
                            try {
                                const sub = candidate.substring(0, i);
                                const parsed = JSON.parse(sub);
                                if (parsed.summary) {
                                    cleanResponse = parsed.summary;
                                    if (parsed.outfit) {
                                        cleanResponse += "\n\nOutfit Tip: " + parsed.outfit;
                                    }
                                    break;
                                }
                            } catch (e) {
                                // continue
                            }
                        }
                    }
                }

                // If JSON extraction failed, try to extract text='...'
                if (cleanResponse.includes('[Event(') || cleanResponse.includes('Event(')) {
                    const textMatch = cleanResponse.match(/text='((?:[^'\\]|\\.)*)'/);
                    if (textMatch) {
                        cleanResponse = textMatch[1].replace(/\\'/g, "'").replace(/\\"/g, '"').replace(/\\n/g, '\n');
                        try {
                            const parsed = JSON.parse(cleanResponse);
                            if (parsed.summary) {
                                cleanResponse = parsed.summary;
                                if (parsed.outfit) {
                                    cleanResponse += "\n\nOutfit Tip: " + parsed.outfit;
                                }
                            }
                        } catch (e) {
                            // Not JSON, keep as text
                        }
                    }
                }
            }

            setMessages(prev => [...prev, { role: 'assistant', content: cleanResponse }]);
        } catch (error) {
            console.error('Chat error:', error);
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: "I'm sorry, I encountered an error. Please try again."
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    const renderContent = (content: string | object) => {
        if (typeof content === 'string') {
            return <p className="whitespace-pre-wrap">{content}</p>;
        }

        // Render structured advice
        const advice = content as any;
        return (
            <div className="space-y-3">
                <p><strong>Summary:</strong> {advice.summary}</p>
                <p><strong>Best Time:</strong> {advice.best_time_match}</p>
                <div className="bg-green-50 p-3 rounded-lg border border-green-100">
                    <p className="font-medium text-green-800 mb-1">Outfit Advice:</p>
                    <p>{advice.outfit}</p>
                </div>
            </div>
        );
    };

    return (
        <div className="flex flex-col h-[500px] bg-white rounded-xl border border-green-200 overflow-hidden shadow-sm">
            {/* Header */}
            <div className="p-4 bg-gradient-to-r from-[var(--eucalyptus)] to-[var(--forest-light)] text-white flex items-center gap-2">
                <Bot className="w-5 h-5" />
                <span className="font-semibold">Chat about {placeName}</span>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
                {messages.map((msg, idx) => (
                    <motion.div
                        key={idx}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
                    >
                        <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${msg.role === 'user' ? 'bg-blue-100 text-blue-600' : 'bg-green-100 text-green-600'
                            }`}>
                            {msg.role === 'user' ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
                        </div>
                        <div className={`max-w-[80%] rounded-2xl p-4 ${msg.role === 'user'
                            ? 'bg-blue-600 text-white rounded-tr-none'
                            : 'bg-white border border-gray-200 rounded-tl-none shadow-sm text-gray-700'
                            }`}>
                            {renderContent(msg.content)}
                        </div>
                    </motion.div>
                ))}
                {isLoading && (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="flex gap-3"
                    >
                        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-green-100 text-green-600 flex items-center justify-center">
                            <Bot className="w-5 h-5" />
                        </div>
                        <div className="bg-white border border-gray-200 rounded-2xl rounded-tl-none p-4 shadow-sm">
                            <Loader2 className="w-5 h-5 animate-spin text-green-600" />
                        </div>
                    </motion.div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <form onSubmit={handleSubmit} className="p-4 bg-white border-t border-gray-100">
                <div className="flex gap-2">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask a follow-up question..."
                        className="flex-1 px-4 py-2 rounded-full border border-gray-300 focus:outline-none focus:border-green-500 focus:ring-1 focus:ring-green-500 transition-all"
                        disabled={isLoading}
                    />
                    <button
                        type="submit"
                        disabled={!input.trim() || isLoading}
                        className="p-2 rounded-full bg-green-600 text-white hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                        <Send className="w-5 h-5" />
                    </button>
                </div>
            </form>
        </div>
    );
}
