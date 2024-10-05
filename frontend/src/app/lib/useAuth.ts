import { useState, useEffect } from 'react';

export interface User {
  id: string;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

interface AuthState {
  isLoggedIn: boolean;
  user: User | null;
  isLoading: boolean;
}

export function useAuth() {
  const [authState, setAuthState] = useState<AuthState>({
    isLoggedIn: false,
    user: null,
    isLoading: true,
  });

  useEffect(() => {
    validateToken();
  }, []);

  const validateToken = async () => {
    const token = localStorage.getItem('authToken');
    if (!token) {
      setAuthState({ isLoggedIn: false, user: null, isLoading: false });
      return;
    }

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/auth/user/`, {
        headers: {
          'Authorization': `Token ${token}`
        },
      });

      if (response.ok) {
        const userData = await response.json();
        setAuthState({
          isLoggedIn: true,
          user: userData,
          isLoading: false,
        });
      } else {
        // Token is invalid
        localStorage.removeItem('authToken');
        setAuthState({ isLoggedIn: false, user: null, isLoading: false });
      }
    } catch (error) {
      console.error('Token validation error:', error);
      setAuthState({ isLoggedIn: false, user: null, isLoading: false });
    }
  };

  const loginWithGitHub = async (code: string) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/auth/github/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code }),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('authToken', data.key);
        await validateToken(); // Fetch user data
        return true;
      } else {
        console.error('GitHub login failed');
        return false;
      }
    } catch (error) {
      console.error('GitHub login error:', error);
      return false;
    }
  };

  const logout = async () => {
    const token = localStorage.getItem('authToken');
    if (token) {
      try {
        await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/auth/logout/`, {
          method: 'POST',
          headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json',
          },
        });
      } catch (error) {
        console.error('Logout error:', error);
      }
    }
    localStorage.removeItem('authToken');
    setAuthState({
      isLoggedIn: false,
      user: null,
      isLoading: false,
    });
  };

  return {
    isLoggedIn: authState.isLoggedIn,
    user: authState.user,
    isLoading: authState.isLoading,
    loginWithGitHub,
    logout,
  };
}