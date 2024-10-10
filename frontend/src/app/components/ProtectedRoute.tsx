import React, { createContext, useContext, useEffect, useState } from 'react';
import { useAuth, User } from '../lib/useAuth';
import { useRouter } from 'next/navigation';

export const UserContext = createContext<User | null>(null);

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, isLoggedIn, isLoading } = useAuth();
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isLoggedIn) {
      router.push('/login');
    }
  }, [isLoggedIn, isLoading, router]);

  useEffect(() => {
    setCurrentUser(user);
    console.log('user', user);
  }, [user]);

  if (isLoading) {
    return <div>Loading...</div>; // Or a proper loading component
  }

  return isLoggedIn ? (
    <UserContext.Provider value={currentUser}>
      {children}
    </UserContext.Provider>
  ) : null;
}

// Create a custom hook to use the UserContext
export const useUser = () => {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserContext.Provider');
  }
  return context;
};
