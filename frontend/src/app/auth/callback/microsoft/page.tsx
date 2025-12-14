'use client';

import { useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { setToken } from '@/lib/auth';

function MicrosoftCallbackContent() {
    const router = useRouter();
    const searchParams = useSearchParams();

    useEffect(() => {
        const accessToken = searchParams.get('access_token');
        const error = searchParams.get('error');

        if (accessToken) {
            setToken(accessToken);
            router.push('/dashboard');
        } else if (error) {
            console.error('Microsoft Auth Error:', error);
            router.push('/login?error=MicrosoftAuthFailed');
        } else {
            router.push('/login');
        }
    }, [router, searchParams]);

    return (
        <div style={{ padding: '2rem', textAlign: 'center' }}>
            <h2>Authenticating with Microsoft...</h2>
            <p>Please wait while we log you in.</p>
        </div>
    );
}

export default function MicrosoftCallbackPage() {
    return (
        <Suspense fallback={<div>Loading...</div>}>
            <MicrosoftCallbackContent />
        </Suspense>
    );
}
