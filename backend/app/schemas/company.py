from pydantic import BaseModel, ConfigDict
from typing import Optional

class CompanyBase(BaseModel):
    name: str
    plan_tier: str = "free"
    billing_email: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyRead(CompanyBase):
    id: int
    name: str
    plan_tier: str
    billing_email: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class UserCompanyRead(BaseModel):
    user_id: int
    company_id: int
    role: str

    model_config = ConfigDict(from_attributes=True)
