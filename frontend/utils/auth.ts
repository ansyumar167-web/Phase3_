// Authentication utility functions for the frontend

/**
 * Get the authenticated user from localStorage
 * @returns User object if authenticated, null otherwise
 */
export function getAuthenticatedUser() {
  if (typeof window === 'undefined') {
    // Server-side, no user available
    return null;
  }

  const userStr = localStorage.getItem('user');
  if (!userStr) {
    return null;
  }

  try {
    return JSON.parse(userStr);
  } catch (error) {
    console.error('Error parsing user data from localStorage:', error);
    // Clear corrupted user data
    localStorage.removeItem('user');
    return null;
  }
}

/**
 * Check if a user is currently authenticated
 * @returns Boolean indicating if user is authenticated
 */
export function isAuthenticated(): boolean {
  return getAuthenticatedUser() !== null;
}

/**
 * Store user data in localStorage after successful authentication
 * @param userData User data to store
 */
export function storeUserData(userData: any): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem('user', JSON.stringify(userData));
  }
}

/**
 * Clear user data from localStorage during logout
 */
export function clearUserData(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('user');
  }
}

/**
 * Get the user ID from stored user data
 * @returns User ID string or null if not authenticated
 */
export function getUserId(): string | null {
  const user = getAuthenticatedUser();
  return user ? user.id || user.user_id || user.sub : null;
}

/**
 * Get the authentication token from stored user data
 * @returns Authentication token string or null if not authenticated
 */
export function getAuthToken(): string | null {
  const user = getAuthenticatedUser();
  return user ? user.access_token || user.token : null;
}

/**
 * Redirect to login page
 */
export function redirectToLogin(): void {
  if (typeof window !== 'undefined') {
    window.location.href = '/login';
  }
}

/**
 * Redirect to chat page after successful authentication
 */
export function redirectToChat(): void {
  if (typeof window !== 'undefined') {
    window.location.href = '/chat';
  }
}