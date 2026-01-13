'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { getToken } from '@/lib/auth';

export default function DashboardPage() {
    const { user, logout, loading } = useAuth();
    const router = useRouter();

    // Client-side route protection (since middleware can't access localStorage)
    useEffect(() => {
        const token = getToken();
        if (!token && !loading) {
            router.push('/login');
        }
    }, [loading, router]);

    if (loading) {
        return <div style={{ padding: '2rem' }}>Loading...</div>;
    }

    // If no user after loading, don't render (will redirect)
    if (!user) {
        return null;
    }

    return (
        <div style={{ padding: '2rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h1>Dashboard</h1>
                <button
                    onClick={logout}
                    disabled={loading}
                    style={{
                        padding: '0.5rem 1rem',
                        cursor: loading ? 'not-allowed' : 'pointer',
                        backgroundColor: '#f44336',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px'
                    }}
                >
                    {loading ? 'Logging out...' : 'Logout'}
                </button>
            </div>
            <div>
                <p><strong>Email:</strong> {user.email}</p>
                <p><strong>User ID:</strong> {user.id}</p>
            </div>
            <p style={{ marginTop: '2rem' }}>Authenticated area – coming soon</p>
        </div>
    );
}
