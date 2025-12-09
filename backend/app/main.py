from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, text
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.engine import engine
from app.db.session import get_session
from app.api import get_v1_router
from app.api.v1.routes_health import router as health_router
from app.api.v1.routes_auth import router as auth_router
from app.models.user import User
from app.models.company import Company
from app.models.user_company import UserCompany
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
    title="Layer Flow Backend",
    debug=True, # Should be from settings
    lifespan=lifespan
)

# Register Routers
app.include_router(health_router, prefix=f"{settings.API_V1_PREFIX}/health", tags=["health"])
app.include_router(auth_router, prefix=settings.API_V1_PREFIX, tags=["auth"])

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
