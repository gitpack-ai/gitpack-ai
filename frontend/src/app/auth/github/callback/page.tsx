'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useSearchParams } from 'next/navigation';
import { useAuth } from '../../../lib/useAuth';

const GitHubCallback = () => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const auth = useAuth();

  useEffect(() => {
    const code = searchParams.get('code');

    if (code) {
      exchangeCodeForToken(code);
    }
  }, [searchParams]);

  const exchangeCodeForToken = async (code: string) => {
    const status = await auth.loginWithGitHub(code);
    if(status)
      router.push('/dashboard')
  };

  return <div>Processing GitHub login...</div>;
};

export default GitHubCallback;