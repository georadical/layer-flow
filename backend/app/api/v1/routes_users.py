from typing import Any
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_session
from app.models.user import User
from app.schemas.user import UserRead

router = APIRouter()

@router.get("/me", response_model=UserRead)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> Any:
    """
    Get current user information.
    """
    return current_user
