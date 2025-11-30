import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { searchQuery } = body;

    console.log('[Next.js API] Received search query:', searchQuery);

    if (!searchQuery) {
      console.error('[Next.js API] Error: Missing search query');
      return NextResponse.json(
        { error: 'Search query is required' },
        { status: 400 }
      );
    }

    // Get backend API URL from environment variable
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    const fullUrl = `${backendUrl}/api/discover`;

    console.log('[Next.js API] Calling backend at:', fullUrl);

    // Call the FastAPI backend
    try {
      const backendResponse = await fetch(fullUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ searchQuery }),
      });

      console.log('[Next.js API] Backend response status:', backendResponse.status);

      if (!backendResponse.ok) {
        const errorData = await backendResponse.json().catch(() => ({}));
        console.error('[Next.js API] Backend API Error:', errorData);
        throw new Error(errorData.detail || 'Backend request failed');
      }

      const data = await backendResponse.json();
      console.log('[Next.js API] Successfully received data from backend');
      return NextResponse.json(data);

    } catch (fetchError) {
      console.error('[Next.js API] Fetch error:', fetchError);

      // Check if backend is running
      if (fetchError instanceof Error && fetchError.message.includes('fetch failed')) {
        console.error('[Next.js API] Backend server is not running at:', backendUrl);
        return NextResponse.json(
          {
            error: 'Backend server not available',
            detail: `Cannot connect to backend at ${backendUrl}. Make sure the backend server is running.`,
            hint: 'Run: cd backend && python main.py'
          },
          { status: 503 }
        );
      }

      throw fetchError;
    }

  } catch (error) {
    console.error('[Next.js API] General error:', error);
    return NextResponse.json(
      {
        error: 'Failed to fetch hidden gems',
        detail: error instanceof Error ? error.message : 'Internal server error'
      },
      { status: 500 }
    );
  }
}
