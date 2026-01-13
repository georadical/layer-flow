
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.models.user import User
from app.db.session import get_session
from sqlmodel import create_engine, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

# Setup DB
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_engine(DATABASE_URL, echo=True)

async def get_test_session():
    async_engine =  create_engine(DATABASE_URL, echo=False) 
    # Wait, create_engine returns Sync engine usually, we need AsyncEngine
    from sqlalchemy.ext.asyncio import create_async_engine
    async_engine = create_async_engine(DATABASE_URL, echo=False)
    
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        
    async_session = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

async def run_test():
    print("STARTING TEST")
    try:
        mock_token = {"access_token": "fake_gh_token"}
        mock_user_resp = MagicMock()
        mock_user_resp.json.return_value = {"email": "gh_public@example.com", "id": 12345}
        
        # Manually create dependency override
        # We need a session generator instance
        async_gen = get_test_session()
        
        async def override_get_session():
             async for s in get_test_session():
                 yield s

        app.dependency_overrides[get_session] = override_get_session

        with patch("app.api.v1.routes_oauth.oauth") as mock_oauth:
            print(f"PATCHED OAUTH: {mock_oauth}")
            mock_oauth.github.authorize_access_token = AsyncMock(return_value=mock_token)
            mock_oauth.github.get = AsyncMock(return_value=mock_user_resp)
            
            transport = ASGITransport(app=app)
            async with AsyncClient(transport=transport, base_url="http://test") as ac:
                print("MAKING REQUEST")
                response = await ac.get("/api/v1/auth/github/callback")
                print(f"RESPONSE STATUS: {response.status_code}")
                if response.status_code != 307:
                     print(f"RESPONSE CONTENT: {response.content}")
                else:
                     print(f"LOCATION: {response.headers['location']}")

    except Exception as e:
        import traceback
        traceback.print_exc()
    print("FINISHED TEST")

if __name__ == "__main__":
    asyncio.run(run_test())
