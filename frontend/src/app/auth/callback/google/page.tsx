'use client';

import { useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { setToken } from '@/lib/auth';

function GoogleCallbackContent() {
    const router = useRouter();
    const searchParams = useSearchParams();

    useEffect(() => {
        const accessToken = searchParams.get('access_token');
        const error = searchParams.get('error');

        if (accessToken) {
            setToken(accessToken);
            router.push('/dashboard');
        } else if (error) {
            // Handle error (maybe redirect to login with error param)
            console.error('Google Auth Error:', error);
            router.push('/login?error=GoogleAuthFailed');
        } else {
            // No token? unexpected state
            router.push('/login');
        }
    }, [router, searchParams]);

    return (
        <div style={{ padding: '2rem', textAlign: 'center' }}>
            <h2>Authenticating...</h2>
            <p>Please wait while we log you in.</p>
        </div>
    );
}

export default function GoogleCallbackPage() {
    return (
        <Suspense fallback={<div>Loading...</div>}>
            <GoogleCallbackContent />
        </Suspense>
    );
}
