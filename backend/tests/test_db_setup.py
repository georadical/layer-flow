import pytest
from sqlalchemy import inspect
from sqlmodel import SQLModel

@pytest.mark.asyncio
async def test_create_tables(test_engine, setup_database):
    """
    Test that the users table is created successfully in the test database.
    """
    async with test_engine.connect() as conn:
        # inspect() requires a sync connection, so we run it in a sync context within the async connection if possible,
        # or use run_sync.
        def get_tables(connection):
            inspector = inspect(connection)
            return inspector.get_table_names()

        table_names = await conn.run_sync(get_tables)
    
    assert "users" in table_names
