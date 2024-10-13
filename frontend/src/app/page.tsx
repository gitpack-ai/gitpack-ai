'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from './lib/useAuth';

export default function Home() {
  const router = useRouter();
  const { isLoggedIn } = useAuth();

  useEffect(() => {
    if (!isLoggedIn) {
      router.push('/login');
    } else {
      router.push('/repositories');
    }
  }, [isLoggedIn, router]);

  return null; // or a loading spinner if you prefer
}

