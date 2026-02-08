// API utility functions for the frontend

import { API_CONFIG, AUTH_CONSTANTS } from '../constants';

/**
 * Makes an authenticated API request
 * @param endpoint The API endpoint to call
 * @param options Request options including method, headers, body, etc.
 * @returns Promise resolving to the response data
 */
export async function authenticatedRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  // Get the user token from localStorage
  const userStr = typeof window !== 'undefined' ? localStorage.getItem(AUTH_CONSTANTS.TOKEN_KEY) : null;
  let token = null;

  if (userStr) {
    try {
      const userData = JSON.parse(userStr);
      // Extract token from the stored auth response
      token = userData.access_token || userData.token; // Adjust property name based on your auth system
    } catch (error) {
      console.error('Error parsing user data:', error);
    }
  }

  const headers = {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
    ...options.headers,
  };

  const response = await fetch(`${API_CONFIG.BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ message: 'API request failed' }));
    throw new Error(errorData.message || `API request failed with status ${response.status}`);
  }

  return response.json();
}

/**
 * Makes a public API request (no authentication required)
 * @param endpoint The API endpoint to call
 * @param options Request options including method, headers, body, etc.
 * @returns Promise resolving to the response data
 */
export async function publicRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  const response = await fetch(`${API_CONFIG.BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ message: 'API request failed' }));
    throw new Error(errorData.message || `API request failed with status ${response.status}`);
  }

  return response.json();
}

/**
 * Specific function for chat endpoint
 */
export async function sendChatMessage(
  userId: string,
  message: string,
  conversationId?: number
): Promise<{ conversation_id: number; response: string; tool_calls: string[] }> {
  const requestBody: { message: string; conversation_id?: number } = { message: message };
  if (conversationId !== undefined) {
    requestBody.conversation_id = conversationId;
  }

  return authenticatedRequest<{ conversation_id: number; response: string; tool_calls: string[] }>(
    `/api/v1/chat`,
    {
      method: 'POST',
      body: JSON.stringify(requestBody),
    }
  );
}

/**
 * Specific function for user authentication (login)
 */
export async function loginUser(
  email: string,
  password: string
): Promise<{ access_token: string; token_type: string; user: any }> {
  return publicRequest<{ access_token: string; token_type: string; user: any }>(
    '/api/login',
    {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    }
  );
}

/**
 * Specific function for user registration
 */
export async function registerUser(
  email: string,
  password: string,
  username: string
): Promise<any> {
  return publicRequest<any>(
    '/api/register',
    {
      method: 'POST',
      body: JSON.stringify({ email, password, username }),
    }
  );
}