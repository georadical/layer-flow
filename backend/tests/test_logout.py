import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.models.user import User
from app.core import jwt

@pytest.mark.asyncio
async def test_logout_success(test_session):
    """
    Test 1 — Logout with valid token
    """
    # Setup: Create user and token
    from app.db.session import get_session
    app.dependency_overrides[get_session] = lambda: test_session
    
    user = User(email="logout_test@example.com", auth_provider="local", is_active=True)
    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)
    
    token = jwt.create_access_token(data={"sub": str(user.id)})
    
    # Action: Call logout
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/v1/logout", headers={
            "Authorization": f"Bearer {token}"
        })
    
    # Assert
    assert response.status_code == 200
    assert response.json() == {"detail": "Logged out successfully"}

@pytest.mark.asyncio
async def test_logout_unauthorized(test_session):
    """
    Test 2 — Logout without token
    """
    from app.db.session import get_session
    app.dependency_overrides[get_session] = lambda: test_session
    
    # Action: Call logout without headers
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/v1/logout")
    
    # Assert
    assert response.status_code == 401
    # Check detail if standard FastAPI security is used
    assert response.json()["detail"] == "Not authenticated"
