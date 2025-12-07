from typing import Optional
from pydantic import BaseModel

class LayerBase(BaseModel):
    project_id: int
    name: str
    data_table: str
    srid: Optional[int] = None
    geometry_type: Optional[str] = None

class LayerRead(LayerBase):
    id: int

    class Config:
        from_attributes = True
