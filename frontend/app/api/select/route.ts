import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { selection } = body;

    console.log('[Next.js API] Received selection:', selection);

    if (!selection) {
      return NextResponse.json(
        { error: 'Selection is required' },
        { status: 400 }
      );
    }

    // Get backend API URL from environment variable
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    const fullUrl = `${backendUrl}/api/select`;

    console.log('[Next.js API] Calling backend at:', fullUrl);

    // Call the FastAPI backend
    try {
      const backendResponse = await fetch(fullUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ selection }),
      });

      console.log('[Next.js API] Backend response status:', backendResponse.status);

      if (!backendResponse.ok) {
        const errorData = await backendResponse.json().catch(() => ({}));
        console.error('[Next.js API] Backend API Error:', errorData);
        throw new Error(errorData.detail || 'Backend request failed');
      }

      const data = await backendResponse.json();
      return NextResponse.json(data);

    } catch (fetchError) {
      console.error('[Next.js API] Fetch error:', fetchError);
      throw fetchError;
    }

  } catch (error) {
    console.error('[Next.js API] General error:', error);
    return NextResponse.json(
      {
        error: 'Failed to process selection',
        detail: error instanceof Error ? error.message : 'Internal server error'
      },
      { status: 500 }
    );
  }
}
