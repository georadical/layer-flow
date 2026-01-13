from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.core import security, jwt
from app.core.config import get_settings
from app.db.session import get_session
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.schemas.auth import Token

router = APIRouter()
settings = get_settings()

@router.post("/signup", response_model=Token)
async def signup(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_session)
) -> Any:
    """
    Create a new user.
    """
    # Check if user exists
    statement = select(User).where(User.email == user_in.email)
    result = await session.exec(statement)
    user = result.first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    # Create user
    user = User(
        email=user_in.email,
        hashed_password=security.hash_password(user_in.password),
        auth_provider=user_in.auth_provider,
        is_active=True
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    # Generate token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    # Find user
    statement = select(User).where(User.email == form_data.username)
    result = await session.exec(statement)
    user = result.first()

    # Authenticate
    if not user or not user.hashed_password or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    
    if not user.is_active:
         raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)) -> Any:
    """
    Logout the current user.
    Since JWTs are stateless, this endpoint doesn't invalidate the token server-side,
    but provides a clear API contract for the frontend to remove the token.
    """
    return {"detail": "Logged out successfully"}
