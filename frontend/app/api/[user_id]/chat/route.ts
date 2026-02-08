import { NextRequest, NextResponse } from 'next/server';

// This is a client-side route handler that will forward requests to the backend API
export async function POST(request: NextRequest) {
  try {
    // Get the request body
    const body = await request.json();
    const { message, conversation_id } = body;

    // Forward the request to the backend API
    // In a real implementation, this would be the actual backend API endpoint
    const backendResponse = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Add any required authentication headers here
        // Authorization: `Bearer ${process.env.BACKEND_API_TOKEN}`, // if needed
      },
      body: JSON.stringify({
        message,
        conversation_id
      }),
    });

    if (!backendResponse.ok) {
      // Handle error from backend
      const errorData = await backendResponse.json().catch(() => ({ error: 'Backend error' }));
      return NextResponse.json(
        { error: errorData.detail || 'Failed to process message', status: backendResponse.status },
        { status: backendResponse.status }
      );
    }

    // Return the response from the backend
    const data = await backendResponse.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Chat API error:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: (error as Error).message },
      { status: 500 }
    );
  }
}

// Optional: GET route to retrieve conversation history
export async function GET(request: NextRequest) {
  try {
    // Extract conversation_id from query parameters
    const url = new URL(request.url);
    const conversation_id = url.searchParams.get('conversation_id');

    if (!conversation_id) {
      return NextResponse.json(
        { error: 'Missing conversation_id parameter' },
        { status: 400 }
      );
    }

    // Forward the request to the backend API to get conversation history
    const backendResponse = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'}/api/conversations/${conversation_id}/messages`, {
      headers: {
        // Add any required authentication headers here
        // Authorization: `Bearer ${process.env.BACKEND_API_TOKEN}`, // if needed
      },
    });

    if (!backendResponse.ok) {
      const errorData = await backendResponse.json().catch(() => ({ error: 'Backend error' }));
      return NextResponse.json(
        { error: errorData.detail || 'Failed to retrieve messages', status: backendResponse.status },
        { status: backendResponse.status }
      );
    }

    const data = await backendResponse.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Get Messages API error:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: (error as Error).message },
      { status: 500 }
    );
  }
}