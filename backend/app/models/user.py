from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, func

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    # Email: unique, nullable=False
    email: str = Field(unique=True, index=True, nullable=False)
    # Hashed Password: nullable for OAuth users
    hashed_password: Optional[str] = Field(default=None, nullable=True)
    # Auth Provider: local, google, etc. Default 'local'
    auth_provider: str = Field(default="local")
    # Provider ID: ID from external provider (e.g. Google sub)
    provider_id: Optional[str] = Field(default=None, nullable=True)
    # Is Active: Default True
    is_active: bool = Field(default=True)
    # Created At: Server default timestamp
    created_at: Optional[datetime] = Field(
        default=None, 
        sa_column_kwargs={"server_default": func.now()}
    )
