from pydantic import BaseModel

class ProjectBase(BaseModel):
    name: str
    owner_id: int

class ProjectRead(ProjectBase):
    id: int

    class Config:
        from_attributes = True
