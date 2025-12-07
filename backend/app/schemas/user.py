from typing import Optional
from pydantic import BaseModel, EmailStr

# Base Schema
class UserBase(BaseModel):
    email: EmailStr

# Create Schema
class UserCreate(UserBase):
    password: str
    auth_provider: str = "local"

# Read Schema
class UserRead(UserBase):
    id: int
    auth_provider: str
    is_active: bool

    class Config:
        from_attributes = True
