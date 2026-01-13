import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
    const token = request.cookies.get('auth_token')?.value ||
        request.headers.get('authorization')?.replace('Bearer ', '');

    // Check if user is trying to access protected routes
    const isProtectedRoute = request.nextUrl.pathname.startsWith('/dashboard');
    const isAuthRoute = request.nextUrl.pathname.startsWith('/login') ||
        request.nextUrl.pathname.startsWith('/signup');

    // Redirect to login if accessing protected route without token
    if (isProtectedRoute && !token) {
        const loginUrl = new URL('/login', request.url);
        return NextResponse.redirect(loginUrl);
    }

    // Redirect to dashboard if accessing auth routes with valid token
    if (isAuthRoute && token) {
        const dashboardUrl = new URL('/dashboard', request.url);
        return NextResponse.redirect(dashboardUrl);
    }

    return NextResponse.next();
}

export const config = {
    matcher: ['/dashboard/:path*', '/login', '/signup'],
};
