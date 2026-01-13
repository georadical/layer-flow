'use client';

import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';

export default function SignupPage() {
    const { signup, error, loading, clearError } = useAuth();
    const [formData, setFormData] = useState({
        email: '',
        confirmEmail: '',
        password: '',
        confirmPassword: ''
    });
    const [errors, setErrors] = useState<{ [key: string]: string }>({});

    const validate = () => {
        const newErrors: { [key: string]: string } = {};

        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(formData.email)) {
            newErrors.email = 'Invalid email address';
        }
        if (formData.email !== formData.confirmEmail) {
            newErrors.confirmEmail = 'Emails do not match';
        }

        // Password validation
        if (formData.password.length < 8) {
            newErrors.password = 'Password must be at least 8 characters';
        }
        if (formData.password !== formData.confirmPassword) {
            newErrors.confirmPassword = 'Passwords do not match';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
        // Clear specific error on change
        if (errors[name]) {
            setErrors(prev => {
                const newErrors = { ...prev };
                delete newErrors[name];
                return newErrors;
            });
        }
        if (error) clearError();
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        clearError();

        if (!validate()) return;

        try {
            await signup(formData.email, formData.password);
        } catch (err) {
            // Error is handled by Auth Context
        }
    };

    const isFormValid = () => {
        return Object.values(formData).every(val => val.trim() !== '') && Object.keys(errors).length === 0;
    };

    return (
        <div style={{ padding: '2rem', maxWidth: '400px', margin: '0 auto' }}>
            <h1>Sign Up</h1>
            {error && <p style={{ color: 'red', marginBottom: '1rem' }}>{error}</p>}

            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                {/* Email */}
                <div>
                    <label style={{ display: 'block', marginBottom: '0.5rem' }}>Email:</label>
                    <input
                        type="email"
                        name="email"
                        required
                        value={formData.email}
                        onChange={handleChange}
                        style={{ width: '100%', padding: '0.5rem', borderColor: errors.email ? 'red' : undefined }}
                    />
                    {errors.email && <small style={{ color: 'red' }}>{errors.email}</small>}
                </div>

                {/* Confirm Email */}
                <div>
                    <label style={{ display: 'block', marginBottom: '0.5rem' }}>Confirm Email:</label>
                    <input
                        type="email"
                        name="confirmEmail"
                        required
                        value={formData.confirmEmail}
                        onChange={handleChange}
                        style={{ width: '100%', padding: '0.5rem', borderColor: errors.confirmEmail ? 'red' : undefined }}
                    />
                    {errors.confirmEmail && <small style={{ color: 'red' }}>{errors.confirmEmail}</small>}
                </div>

                {/* Password */}
                <div>
                    <label style={{ display: 'block', marginBottom: '0.5rem' }}>Password:</label>
                    <input
                        type="password"
                        name="password"
                        required
                        value={formData.password}
                        onChange={handleChange}
                        style={{ width: '100%', padding: '0.5rem', borderColor: errors.password ? 'red' : undefined }}
                    />
                    {errors.password && <small style={{ color: 'red' }}>{errors.password}</small>}
                </div>

                {/* Confirm Password */}
                <div>
                    <label style={{ display: 'block', marginBottom: '0.5rem' }}>Confirm Password:</label>
                    <input
                        type="password"
                        name="confirmPassword"
                        required
                        value={formData.confirmPassword}
                        onChange={handleChange}
                        style={{ width: '100%', padding: '0.5rem', borderColor: errors.confirmPassword ? 'red' : undefined }}
                    />
                    {errors.confirmPassword && <small style={{ color: 'red' }}>{errors.confirmPassword}</small>}
                </div>

                <button
                    type="submit"
                    disabled={loading || !isFormValid()}
                    style={{
                        padding: '0.5rem',
                        cursor: (loading || !isFormValid()) ? 'not-allowed' : 'pointer',
                        opacity: (loading || !isFormValid()) ? 0.7 : 1
                    }}
                >
                    {loading ? 'Signing up...' : 'Sign Up'}
                </button>
            </form>
        </div>
    );
}
