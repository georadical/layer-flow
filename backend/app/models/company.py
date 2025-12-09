from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, DateTime, func, String

if TYPE_CHECKING:
    from app.models.user_company import UserCompany

class Company(SQLModel, table=True):
    __tablename__ = "companies"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(sa_column=Column(String, unique=True, nullable=False))
    plan_tier: str = Field(default="free", nullable=False)
    billing_email: Optional[str] = Field(default=None, nullable=True)
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )

    users: List["UserCompany"] = Relationship(back_populates="company", sa_relationship_kwargs={"cascade": "all, delete"})
