import { NextRequest, NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  // Define protected routes
  const protectedRoutes = ['/chat'];
  const isProtectedRoute = protectedRoutes.some(route =>
    request.nextUrl.pathname.startsWith(route)
  );

  // If it's a protected route, check for authentication
  if (isProtectedRoute) {
    // Check if user is authenticated by looking for user data in localStorage
    // In a real implementation, this would involve checking cookies or headers
    // For this example, we'll just check if there's a user in localStorage
    // which would be set after successful login

    // For server-side, we can't directly access localStorage
    // So we'll check for a session cookie or token in headers
    const userToken = request.cookies.get('auth-token') || request.headers.get('authorization');

    // For this implementation, we'll allow access if there's any auth token
    // In a real app, you'd validate the token with your backend
    if (!userToken) {
      // Redirect to login if not authenticated
      return NextResponse.redirect(new URL('/login', request.url));
    }
  }

  return NextResponse.next();
}

// Apply middleware to specific paths
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};