from typing import Optional
from sqlmodel import SQLModel, Field

class ExampleModel(SQLModel, table=True):
    __tablename__ = "example_layer"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    
    # Geometry field: Stored as WKT string initially.
    # In a production PostGIS setup with GeoAlchemy2, this would be:
    # geom: Any = Field(sa_column=Column(Geometry("POINT")))
    geom: Optional[str] = None
