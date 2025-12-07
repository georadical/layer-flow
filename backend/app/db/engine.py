from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from app.core.config import get_settings

settings = get_settings()

# Ensure we are using the async driver
if not settings.DATABASE_URL.startswith("postgresql+asyncpg"):
    raise ValueError("DATABASE_URL must be set to use postgresql+asyncpg scheme")

# Create the Async Engine
# echo=False: Disable SQL query logging (enable for debugging)
# pool_pre_ping=True: Check connection health before usage
engine = AsyncEngine(
    create_engine(
        settings.DATABASE_URL,
        echo=False,
        future=True,
        pool_pre_ping=True,
    )
)
