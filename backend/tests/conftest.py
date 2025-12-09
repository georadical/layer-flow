import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
import sys
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Import models to ensure they are registered in SQLModel.metadata
from app.models.user import User

# Use SQLite in-memory database for testing (Async)
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture(scope="session")
async def test_engine():
    """
    Creates an asynchronous SQLite engine for testing.
    """
    engine = create_async_engine(
        SQLALCHEMY_DATABASE_URL, 
        echo=False,
        connect_args={"check_same_thread": False}
    )
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def setup_database(test_engine):
    """
    Create tables before each test function and drop them afterwards.
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def test_session(test_engine, setup_database):
    """
    Provides an asynchronous transactional session for each test.
    """
    async_session = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
