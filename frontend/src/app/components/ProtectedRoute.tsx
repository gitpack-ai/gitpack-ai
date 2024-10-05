import React, { createContext, useContext } from 'react';
import { useAuth, User } from '../lib/useAuth';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';


export const UserContext = createContext<User | null>(null);

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, isLoggedIn, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isLoggedIn) {
      router.push('/login');
    }
  }, [isLoggedIn, isLoading, router]);

  if (isLoading) {
    return <div>Loading...</div>; // Or a proper loading component
  }

  return isLoggedIn ? (
    <UserContext.Provider value={user}>
      {children}
    </UserContext.Provider>
  ) : null;
}

// Create a custom hook to use the UserContext
export const useUser = () => useContext(UserContext);
