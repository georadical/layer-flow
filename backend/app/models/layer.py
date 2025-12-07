from typing import Optional
from sqlmodel import SQLModel, Field

class Layer(SQLModel, table=True):
    __tablename__ = "layers"

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="projects.id")
    name: str = Field(index=True)
    data_table: str
    srid: Optional[int] = None
    geometry_type: Optional[str] = None
