from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, text
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.engine import engine
from app.db.session import get_session
from app.api import get_v1_router
from app.models.user import User
from app.models.project import Project
from app.models.layer import Layer
from app.models.example_model import ExampleModel

# Configure logging early
configure_logging()

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize Database
    async with engine.begin() as conn:
        # Create all tables defined in SQLModel metadata
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    # Shutdown: Add cleanup code here if needed
    await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    debug=settings.DEBUG,
    lifespan=lifespan
)

# Include v1 router
app.include_router(get_v1_router(), prefix=settings.API_V1_PREFIX)

@app.get("/")
def root():
    """
    Root endpoint returning a welcome message.
    """
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "docs": "/docs"
    }

@app.get("/test-db")
async def test_db(session: AsyncSession = Depends(get_session)):
    """
    Test endpoint to verify database connection.
    """
    try:
        # Execute a simple query
        await session.exec(text("SELECT 1"))
        return {"connected": True}
    except Exception as e:
        return {"connected": False, "error": str(e)}
