// Authentication helpers
// NOTE: Storing JWTs in localStorage is susceptible to XSS attacks.
// For a production-grade application, consider using HTTP-only cookies
// to prevent JavaScript access to the token.
// This implementation is for MVP purposes only.

const TOKEN_KEY = 'auth_token';

export const setToken = (token: string): void => {
    if (typeof window !== 'undefined') {
        localStorage.setItem(TOKEN_KEY, token);
    }
};

export const getToken = (): string | null => {
    if (typeof window !== 'undefined') {
        return localStorage.getItem(TOKEN_KEY);
    }
    return null;
};

export const removeToken = (): void => {
    if (typeof window !== 'undefined') {
        localStorage.removeItem(TOKEN_KEY);
    }
};

export const isAuthenticated = (): boolean => {
    return !!getToken();
};
