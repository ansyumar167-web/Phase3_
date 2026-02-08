import { NextRequest, NextResponse } from 'next/server';

// Login route
export async function POST(request: NextRequest) {
  try {
    const { pathname } = new URL(request.url);

    // Determine if this is a login or register request based on the path
    if (pathname.includes('/api/login')) {
      return await handleLogin(request);
    } else if (pathname.includes('/api/register')) {
      return await handleRegister(request);
    } else {
      return NextResponse.json(
        { error: 'Invalid endpoint' },
        { status: 404 }
      );
    }
  } catch (error) {
    console.error('Auth API error:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: (error as Error).message },
      { status: 500 }
    );
  }
}

async function handleLogin(request: NextRequest) {
  try {
    const body = await request.json();
    const { email, password } = body;

    // Validate input
    if (!email || !password) {
      return NextResponse.json(
        { error: 'Email and password are required' },
        { status: 400 }
      );
    }

    // In a real implementation, this would call the actual backend authentication API
    // For this example, we'll simulate the authentication process
    // and return a mock user object

    // This is a placeholder - in a real app, you would call your backend API
    const backendResponse = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'}/api/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    if (backendResponse.ok) {
      const userData = await backendResponse.json();

      // In a real app, you would set cookies or return authentication tokens
      // For this example, we'll return a mock user object
      const mockUser = {
        id: 'user_' + Math.random().toString(36).substr(2, 9),
        email: email,
        username: email.split('@')[0],
        created_at: new Date().toISOString(),
      };

      return NextResponse.json({
        access_token: 'mock-jwt-token-' + Math.random().toString(36).substr(2, 9),
        token_type: 'bearer',
        user: mockUser
      });
    } else {
      const errorData = await backendResponse.json().catch(() => ({ detail: 'Invalid credentials' }));
      return NextResponse.json(
        { error: errorData.detail || 'Invalid credentials' },
        { status: 401 }
      );
    }
  } catch (error) {
    console.error('Login error:', error);
    return NextResponse.json(
      { error: 'Login failed' },
      { status: 500 }
    );
  }
}

async function handleRegister(request: NextRequest) {
  try {
    const body = await request.json();
    const { email, password, username } = body;

    // Validate input
    if (!email || !password || !username) {
      return NextResponse.json(
        { error: 'Email, password, and username are required' },
        { status: 400 }
      );
    }

    // In a real implementation, this would call the actual backend registration API
    // For this example, we'll simulate the registration process

    // This is a placeholder - in a real app, you would call your backend API
    const backendResponse = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'}/api/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password, username }),
    });

    if (backendResponse.ok) {
      const result = await backendResponse.json();

      // Return success response
      return NextResponse.json({
        id: 'user_' + Math.random().toString(36).substr(2, 9),
        email: email,
        username: username
      });
    } else {
      const errorData = await backendResponse.json().catch(() => ({ detail: 'Registration failed' }));
      return NextResponse.json(
        { error: errorData.detail || 'Registration failed' },
        { status: 400 }
      );
    }
  } catch (error) {
    console.error('Registration error:', error);
    return NextResponse.json(
      { error: 'Registration failed' },
      { status: 500 }
    );
  }
}