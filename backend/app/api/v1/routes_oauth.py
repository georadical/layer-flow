from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core import security, jwt
from app.core.config import get_settings
from app.core.oauth import oauth
from app.db.session import get_session
from app.models.user import User
from app.schemas.auth import Token

router = APIRouter()
settings = get_settings()

@router.get("/google/login")
async def google_login(request: Request):
    """
    Redirects user to Google OAuth login.
    """
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback")
async def google_callback(
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    """
    Handle Google OAuth callback.
    """
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")
    
    if not user_info:
         # Fallback try to get userinfo if not in token response
         user_info = await oauth.google.userinfo(token=token)

    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to get user info from Google")

    email = user_info.get("email")
    sub = user_info.get("sub") # Provider ID

    if not email:
        raise HTTPException(status_code=400, detail="Email not found in Google account")

    return await _process_oauth_login(session, email, "google", sub)

@router.get("/microsoft/login")
async def microsoft_login(request: Request):
    """
    Redirects user to Microsoft OAuth login.
    """
    redirect_uri = settings.MICROSOFT_REDIRECT_URI
    return await oauth.microsoft.authorize_redirect(request, redirect_uri)

@router.get("/microsoft/callback")
async def microsoft_callback(
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    """
    Handle Microsoft OAuth callback.
    """
    token = await oauth.microsoft.authorize_access_token(request)
    user_info = token.get("userinfo")
    
    if not user_info:
         user_info = await oauth.microsoft.userinfo(token=token)

    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to get user info from Microsoft")

    email = user_info.get("email")
    sub = user_info.get("sub")

    if not email:
        raise HTTPException(status_code=400, detail="Email not found in Microsoft account")
    
    return await _process_oauth_login(session, email, "microsoft", sub)

@router.get("/github/login")
async def github_login(request: Request):
    """
    Redirects user to GitHub OAuth login.
    """
    redirect_uri = settings.GITHUB_REDIRECT_URI
    return await oauth.github.authorize_redirect(request, redirect_uri)

@router.get("/github/callback")
async def github_callback(
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    """
    Handle GitHub OAuth callback.
    """
    token = await oauth.github.authorize_access_token(request)
    resp = await oauth.github.get("user", token=token)
    user_info = resp.json()

    # GitHub email might be private, fetch explicitly if needed
    email = user_info.get("email")
    sub = str(user_info.get("id")) # GitHub ID is integer

    if not email:
        # Fetch emails
        resp_emails = await oauth.github.get("user/emails", token=token)
        emails = resp_emails.json()
        primary_email = next((e for e in emails if e["primary"] and e["verified"]), None)
        if primary_email:
             email = primary_email["email"]

    if not email:
        raise HTTPException(status_code=400, detail="Email not found in GitHub account")
    
    return await _process_oauth_login(session, email, "github", sub)

async def _process_oauth_login(session: AsyncSession, email: str, provider: str, provider_id: str):
    stmt = select(User).where(User.email == email)
    result = await session.exec(stmt)
    user = result.first()

    if not user:
        user = User(
            email=email,
            auth_provider=provider,
            provider_id=provider_id,
            is_active=True,
            hashed_password=None
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
    else:
        # Update provider info if logging in with provider for first time
        if not user.provider_id and user.auth_provider == provider:
             user.provider_id = provider_id
             session.add(user)
             await session.commit()
             await session.refresh(user)

    # Generate Access Token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    # Redirect to frontend callback
    frontend_url = f"http://localhost:3000/auth/callback/{provider}"
    return RedirectResponse(url=f"{frontend_url}?access_token={access_token}")
