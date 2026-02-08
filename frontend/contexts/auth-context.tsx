'use client';

import { createContext, useContext, useState, ReactNode, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { publicRequest } from '../utils/api';

// Define the user type
interface User {
  id: string;
  email: string;
  username: string;
}

// Define the auth response type
interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// Define the context type
interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
  register: (email: string, password: string, username: string) => Promise<boolean>;
  loading: boolean;
}

// Create the context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Create the provider component
export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  // Check if user is already logged in on initial load
  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      try {
        const parsedUser = JSON.parse(storedUser);
        setUser(parsedUser);
      } catch (error) {
        console.error('Error parsing stored user:', error);
        localStorage.removeItem('user');
      }
    }
    setLoading(false);
  }, []);

  const login = async (email: string, password: string): Promise<boolean> => {
    setLoading(true);
    try {
      // Use the API utility function which handles base URL correctly
      const data = await publicRequest('/api/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      }) as AuthResponse;

      // Store complete auth data (including token) in localStorage and update context
      localStorage.setItem('user', JSON.stringify(data));
      setUser(data.user);

      // Set a cookie for the middleware to detect authentication
      document.cookie = `auth-token=${data.access_token}; path=/; max-age=1800; SameSite=Lax`; // 30 min expiry

      router.push('/chat');
      return true;
    } catch (error) {
      console.error('Login error:', error);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const register = async (email: string, password: string, username: string): Promise<boolean> => {
    setLoading(true);
    try {
      // Use the API utility function which handles base URL correctly
      await publicRequest('/api/register', {
        method: 'POST',
        body: JSON.stringify({ email, password, username }),
      });

      // After registration, redirect to login
      router.push('/login');
      return true;
    } catch (error) {
      console.error('Registration error:', error);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('user');
    // Clear the auth cookie as well
    document.cookie = 'auth-token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT;';
    setUser(null);
    router.push('/login');
  };

  const value = {
    user,
    login,
    logout,
    register,
    loading,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

// Create a custom hook to use the auth context
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}