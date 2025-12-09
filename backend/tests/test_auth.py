import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.models.user import User

@pytest.mark.asyncio
async def test_signup(test_session, test_engine):
    """
    Test user signup.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Override the dependency to use the test session
        app.dependency_overrides[test_session] = lambda: test_session 
        # Note: The above override attempt is slightly flawed for async tests 
        # because FastAPI deps are tricky with pytest-asyncio and session overrides.
        # A better approach is to rely on the fact that we swap the engine/session in conftest 
        # or just test the logic directly if possible. 
        # However, for full integration tests, let's try a simpler approach if the above is complex.
        # We will assume standard dependency injection works if we override get_session.
        
        from app.db.session import get_session
        app.dependency_overrides[get_session] = lambda: test_session
        
        response = await ac.post("/api/v1/signup", json={
            "email": "signup@example.com",
            "password": "strongpassword"
        })
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "signup@example.com"
    assert "id" in data
    assert "hashed_password" not in data

    # Verify DB
    from sqlmodel import select
    statement = select(User).where(User.email == "signup@example.com")
    result = await test_session.exec(statement)
    user = result.first()
    assert user is not None

@pytest.mark.asyncio
async def test_duplicate_email(test_session):
    """
    Test that signing up with a duplicate email fails.
    """
    from app.db.session import get_session
    app.dependency_overrides[get_session] = lambda: test_session
    
    # Create first user
    user = User(email="duplicate@example.com", hashed_password="pw", auth_provider="local")
    test_session.add(user)
    test_session.commit()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/v1/signup", json={
            "email": "duplicate@example.com",
            "password": "newpassword"
        })
        
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

@pytest.mark.asyncio
async def test_login(test_session):
    """
    Test user login.
    """
    from app.db.session import get_session
    from app.core.security import hash_password
    app.dependency_overrides[get_session] = lambda: test_session

    password = "loginpass"
    hashed = hash_password(password)
    user = User(email="login@example.com", hashed_password=hashed, auth_provider="local")
    test_session.add(user)
    test_session.commit()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/v1/login", data={
            "username": "login@example.com",
            "password": password
        })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_wrong_password(test_session):
    """
    Test login with incorrect password.
    """
    from app.db.session import get_session
    from app.core.security import hash_password
    app.dependency_overrides[get_session] = lambda: test_session

    user = User(email="wrong@example.com", hashed_password=hash_password("pw"), auth_provider="local")
    test_session.add(user)
    test_session.commit()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/v1/login", data={
            "username": "wrong@example.com",
            "password": "wrongpass"
        })

    # Expect 400 as per implementation
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_protected_route(test_session):
    """
    Test accessing a protected route with a valid token.
    """
    from app.db.session import get_session
    from app.core import jwt
    from fastapi import APIRouter, Depends
    from app.core.deps import get_current_user
    from app.schemas.user import UserRead
    
    app.dependency_overrides[get_session] = lambda: test_session
    
    # 1. Create a dummy protected route for testing
    router = APIRouter()
    @router.get("/auth-test", response_model=UserRead)
    async def auth_test_endpoint(current_user: User = Depends(get_current_user)):
        return current_user
    
    app.include_router(router, prefix="/api/v1")

    # 2. Create user and token
    user = User(email="token@example.com", auth_provider="local")
    test_session.add(user)
    await test_session.commit() 
    await test_session.refresh(user)
    
    token = jwt.create_access_token(data={"sub": str(user.id)})

    # 3. Call endpoint
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/auth-test", headers={
            "Authorization": f"Bearer {token}"
        })

    assert response.status_code == 200
    assert response.json()["email"] == "token@example.com"
