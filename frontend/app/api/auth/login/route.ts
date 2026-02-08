import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { email, password } = await request.json();

    // Validate input
    if (!email || !password) {
      return NextResponse.json(
        { error: 'Email and password are required' },
        { status: 400 }
      );
    }

    // Forward the request to the backend authentication service
    const backendResponse = await fetch(`${process.env.BACKEND_API_URL || 'http://localhost:8000'}/api/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    if (!backendResponse.ok) {
      const errorData = await backendResponse.json().catch(() => ({ detail: 'Login failed' }));
      return NextResponse.json(
        { error: errorData.detail || 'Login failed' },
        { status: backendResponse.status }
      );
    }

    const data = await backendResponse.json();

    // Return the authentication data
    return NextResponse.json({
      access_token: data.access_token,
      token_type: data.token_type,
      user: data.user
    });
  } catch (error) {
    console.error('Login API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}