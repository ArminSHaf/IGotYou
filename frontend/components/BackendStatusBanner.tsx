'use client';

import { useEffect, useState } from 'react';
import { AlertCircle, CheckCircle, RefreshCw, Terminal } from 'lucide-react';

export function BackendStatusBanner() {
  const [status, setStatus] = useState<'checking' | 'online' | 'offline'>('checking');
  const [showDetails, setShowDetails] = useState(false);

  const checkBackendStatus = async () => {
    try {
      const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(backendUrl, {
        method: 'GET',
        signal: AbortSignal.timeout(3000), // 3 second timeout
      });

      if (response.ok) {
        setStatus('online');
      } else {
        setStatus('offline');
      }
    } catch (error) {
      setStatus('offline');
    }
  };

  useEffect(() => {
    checkBackendStatus();
    // Check status every 10 seconds
    const interval = setInterval(checkBackendStatus, 10000);
    return () => clearInterval(interval);
  }, []);

  if (status === 'online') {
    return null; // Don't show banner when backend is online
  }

  if (status === 'checking') {
    return (
      <div className="bg-[var(--accent-blue)]/5 border-b border-[var(--border-default)] px-4 py-2.5">
        <div className="container mx-auto flex items-center gap-2 text-[var(--accent-blue)]">
          <RefreshCw className="w-4 h-4 animate-spin" />
          <span className="text-sm">Checking backend status...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-amber-50 border-b border-amber-200 px-4 py-2.5">
      <div className="container mx-auto">
        <div className="flex items-start justify-between gap-4">
          <div className="flex items-start gap-2 flex-1">
            <AlertCircle className="w-4 h-4 text-amber-600 mt-0.5 flex-shrink-0" />
            <div className="flex-1">
              <div className="flex items-center gap-3">
                <span className="text-sm font-semibold text-amber-900">
                  Backend Server Not Running
                </span>
                <button
                  onClick={() => setShowDetails(!showDetails)}
                  className="text-xs text-amber-700 hover:text-amber-900 font-medium"
                >
                  {showDetails ? 'Hide' : 'Show'} Instructions
                </button>
                <button
                  onClick={checkBackendStatus}
                  className="inline-flex items-center gap-1 text-xs text-amber-700 hover:text-amber-900 font-medium"
                >
                  <RefreshCw className="w-3 h-3" />
                  Recheck
                </button>
              </div>

              {showDetails && (
                <div className="mt-3 space-y-2">
                  <p className="text-sm text-amber-800">
                    The search functionality requires the backend API server. Please start it in a new terminal:
                  </p>

                  <div className="bg-[var(--gray-900)] rounded-md p-3 font-mono text-sm">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2 text-[var(--gray-400)]">
                        <Terminal className="w-3.5 h-3.5" />
                        <span className="text-xs">Terminal</span>
                      </div>
                      <button
                        onClick={() => {
                          navigator.clipboard.writeText('cd backend\npython main.py');
                        }}
                        className="text-xs text-[var(--accent-green)] hover:opacity-80 px-2 py-1 rounded bg-[var(--gray-800)]"
                      >
                        Copy
                      </button>
                    </div>
                    <code className="text-[var(--accent-green)]">
                      <div>$ cd backend</div>
                      <div>$ python main.py</div>
                    </code>
                  </div>

                  <div className="flex items-start gap-2 text-xs text-amber-800 bg-amber-100 rounded-md p-2.5">
                    <CheckCircle className="w-3.5 h-3.5 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="font-medium mb-1">After starting the backend, you should see:</p>
                      <code className="text-xs bg-white px-2 py-1 rounded">
                        🚀 Starting I Got You Backend API Server
                      </code>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
