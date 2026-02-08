import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { email, password, username } = await request.json();

    // Validate input
    if (!email || !password || !username) {
      return NextResponse.json(
        { error: 'Email, password, and username are required' },
        { status: 400 }
      );
    }

    // Forward the request to the backend registration service
    const backendResponse = await fetch(`${process.env.BACKEND_API_URL || 'http://localhost:8000'}/api/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password, username }),
    });

    if (!backendResponse.ok) {
      const errorData = await backendResponse.json().catch(() => ({ detail: 'Registration failed' }));
      return NextResponse.json(
        { error: errorData.detail || 'Registration failed' },
        { status: backendResponse.status }
      );
    }

    const data = await backendResponse.json();

    // Return the registration result
    return NextResponse.json({
      id: data.id,
      email: data.email,
      username: data.username
    });
  } catch (error) {
    console.error('Registration API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}