'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { apiFetch } from '@/lib/api';
import { getToken, setToken as saveToken, removeToken } from '@/lib/auth';

interface User {
    id: string;
    email: string;
}

interface AuthContextType {
    user: User | null;
    loading: boolean;
    error: string | null;
    login: (email: string, password: string) => Promise<void>;
    signup: (email: string, password: string) => Promise<void>;
    logout: () => Promise<void>;
    clearError: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const router = useRouter();

    // Initialize auth state on mount
    useEffect(() => {
        const initAuth = async () => {
            const token = getToken();
            if (token) {
                try {
                    // Fetch current user from backend
                    const userData = await apiFetch<User>('/users/me');
                    setUser(userData);
                } catch (err) {
                    // Token is invalid, clear it
                    removeToken();
                    setUser(null);
                }
            }
            setLoading(false);
        };

        initAuth();
    }, []);

    const login = async (email: string, password: string) => {
        setError(null);
        setLoading(true);

        try {
            const formData = new URLSearchParams();
            formData.append('username', email);
            formData.append('password', password);

            const data = await apiFetch<{ access_token: string }>('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formData.toString(),
            });

            saveToken(data.access_token);

            // Fetch user data
            const userData = await apiFetch<User>('/users/me');
            setUser(userData);

            router.push('/dashboard');
        } catch (err: any) {
            setError(err.message || 'Login failed');
            throw err;
        } finally {
            setLoading(false);
        }
    };

    const signup = async (email: string, password: string) => {
        setError(null);
        setLoading(true);

        try {
            const data = await apiFetch<{ access_token: string }>('/signup', {
                method: 'POST',
                body: JSON.stringify({ email, password }),
            });

            if (data.access_token) {
                saveToken(data.access_token);

                // Fetch user data
                const userData = await apiFetch<User>('/users/me');
                setUser(userData);

                router.push('/dashboard');
            } else {
                router.push('/login');
            }
        } catch (err: any) {
            setError(err.message || 'Signup failed');
            throw err;
        } finally {
            setLoading(false);
        }
    };

    const logout = async () => {
        setLoading(true);
        try {
            await apiFetch('/logout', { method: 'POST' });
        } catch (error) {
            console.error('Logout failed:', error);
        } finally {
            removeToken();
            setUser(null);
            setLoading(false);
            router.push('/login');
        }
    };

    const clearError = () => setError(null);

    return (
        <AuthContext.Provider value={{ user, loading, error, login, signup, logout, clearError }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}
