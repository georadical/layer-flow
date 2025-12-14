'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiFetch } from '@/lib/api';
import { setToken } from '@/lib/auth';

export default function LoginPage() {
    const router = useRouter();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            // Backend expects OAuth2 form data
            const formData = new URLSearchParams();
            formData.append('username', email); // backend usually expects username field for OAuth2
            formData.append('password', password);

            const data = await apiFetch<{ access_token: string }>('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formData.toString(),
            });

            setToken(data.access_token);
            router.push('/dashboard');
        } catch (err: any) {
            setError(err.message || 'Login failed');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ padding: '2rem', maxWidth: '400px', margin: '0 auto' }}>
            <h1>Login</h1>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <div>
                    <label style={{ display: 'block', marginBottom: '0.5rem' }}>Email:</label>
                    <input
                        type="email"
                        required
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        style={{ width: '100%', padding: '0.5rem' }}
                    />
                </div>
                <div>
                    <label style={{ display: 'block', marginBottom: '0.5rem' }}>Password:</label>
                    <input
                        type="password"
                        required
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        style={{ width: '100%', padding: '0.5rem' }}
                    />
                </div>
                <button type="submit" disabled={loading} style={{ padding: '0.5rem', cursor: 'pointer' }}>
                    {loading ? 'Logging in...' : 'Login'}
                </button>
            </form>

            <div style={{ marginTop: '1rem', textAlign: 'center' }}>
                <p>Or</p>
                <button
                    onClick={() => window.location.href = `${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1'}/auth/google/login`}
                    style={{
                        marginTop: '0.5rem',
                        padding: '0.5rem',
                        cursor: 'pointer',
                        width: '100%',
                        backgroundColor: '#DB4437',
                        color: 'white',
                        border: 'none'
                    }}
                >
                    Continue with Google
                </button>
                <button
                    onClick={() => window.location.href = `${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1'}/auth/microsoft/login`}
                    style={{
                        marginTop: '0.5rem',
                        padding: '0.5rem',
                        cursor: 'pointer',
                        width: '100%',
                        backgroundColor: '#0078D4',
                        color: 'white',
                        border: 'none'
                    }}
                >
                    Continue with Microsoft
                </button>
                <button
                    onClick={() => window.location.href = `${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1'}/auth/github/login`}
                    style={{
                        marginTop: '0.5rem',
                        padding: '0.5rem',
                        cursor: 'pointer',
                        width: '100%',
                        backgroundColor: '#24292e',
                        color: 'white',
                        border: 'none'
                    }}
                >
                    Continue with GitHub
                </button>
            </div>
        </div>
    );
}
