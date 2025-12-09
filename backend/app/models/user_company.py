from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.company import Company

class UserCompany(SQLModel, table=True):
    __tablename__ = "user_company"

    user_id: int = Field(foreign_key="users.id", primary_key=True)
    company_id: int = Field(foreign_key="companies.id", primary_key=True)
    role: str = Field(default="member", nullable=False)

    user: "User" = Relationship(back_populates="companies")
    company: "Company" = Relationship(back_populates="users")
