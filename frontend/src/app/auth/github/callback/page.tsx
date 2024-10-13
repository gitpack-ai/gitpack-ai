'use client';

import { useEffect, Suspense } from 'react';
import { useRouter } from 'next/navigation';
import { useSearchParams } from 'next/navigation';
import { useAuth } from '../../../lib/useAuth';

const GitHubCallbackContent = () => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const auth = useAuth();

  useEffect(() => {
    const exchangeCodeForToken = async (code: string) => {
      const status = await auth.loginWithGitHub(code);
      if (status) {
        router.push('/repositories');
      }
    };

    const code = searchParams.get('code');

    if (code) {
      exchangeCodeForToken(code);
    }
  }, [searchParams, auth, router]);

  return <div>Processing GitHub login...</div>;
};

const GitHubCallback = () => {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <GitHubCallbackContent />
    </Suspense>
  );
};

export default GitHubCallback;