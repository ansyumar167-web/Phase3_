'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { publicRequest } from '../utils/api';

interface User {
  id: string;
  email: string;
  username: string;
}

interface LoginResponse {
  user: User;
  access_token: string;
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<boolean>;
  register: (email: string, password: string, username: string) => Promise<boolean>;
  logout: () => void;
  isAuthenticated: boolean;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check if user is already logged in on initial load
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      try {
        const parsedUserData = JSON.parse(storedUser);
        // Extract user from the stored auth response
        const user = parsedUserData.user || parsedUserData;
        setUser(user);
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
      const userData = await publicRequest('/api/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      }) as LoginResponse;

      setUser(userData.user);
      // Store complete auth data (including token) for authenticated requests
      localStorage.setItem('user', JSON.stringify(userData));

      // Set a cookie for the middleware to detect authentication
      document.cookie = `auth-token=${userData.access_token}; path=/; max-age=1800; SameSite=Lax`; // 30 min expiry

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

      // After registration, typically you'd need to log in
      // For this example, we'll just redirect to login
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
    setUser(null);
    localStorage.removeItem('user');
    // Clear the auth cookie as well
    document.cookie = 'auth-token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT;';
    router.push('/login');
  };

  const isAuthenticated = !!user;

  const value = {
    user,
    login,
    register,
    logout,
    isAuthenticated,
    loading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}