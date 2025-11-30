import { NextResponse } from 'next/server';

export async function POST(request: Request) {
    try {
        const body = await request.json();
        console.log('[Next.js API] Received chat message:', body.message);

        const backendUrl = 'http://localhost:8000/api/chat';
        console.log('[Next.js API] Calling backend at:', backendUrl);

        const response = await fetch(backendUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
        });

        if (!response.ok) {
            console.error('[Next.js API] Backend returned error:', response.status);
            return NextResponse.json(
                { error: 'Backend error' },
                { status: response.status }
            );
        }

        const data = await response.json();
        console.log('[Next.js API] Successfully received response from backend');

        return NextResponse.json(data);
    } catch (error) {
        console.error('[Next.js API] Error proxying chat request:', error);
        return NextResponse.json(
            { error: 'Internal server error' },
            { status: 500 }
        );
    }
}
