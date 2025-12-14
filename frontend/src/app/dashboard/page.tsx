'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { isAuthenticated, removeToken } from '@/lib/auth';
import { apiFetch } from '@/lib/api';

export default function DashboardPage() {
    const router = useRouter();
    const [authorized, setAuthorized] = useState(false);

    const [logoutLoading, setLogoutLoading] = useState(false);

    useEffect(() => {
        if (!isAuthenticated()) {
            router.push('/login');
        } else {
            setAuthorized(true);
        }
    }, [router]);

    if (!authorized) {
        return <div style={{ padding: '2rem' }}>Redirecting...</div>;
    }

    const handleLogout = async () => {
        setLogoutLoading(true);
        try {
            // Attempt to call backend logout
            // We ignore the result as we want to logout client-side regardless
            await apiFetch('/logout', { method: 'POST' });
        } catch (error) {
            console.error('Logout failed:', error);
        } finally {
            removeToken();
            setLogoutLoading(false);
            router.push('/login');
        }
    };

    return (
        <div style={{ padding: '2rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h1>Dashboard</h1>
                <button
                    onClick={handleLogout}
                    disabled={logoutLoading}
                    style={{
                        padding: '0.5rem 1rem',
                        cursor: logoutLoading ? 'not-allowed' : 'pointer',
                        backgroundColor: '#f44336',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px'
                    }}
                >
                    {logoutLoading ? 'Logging out...' : 'Logout'}
                </button>
            </div>
            <p>Authenticated area – coming soon</p>
        </div>
    );
}
