import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.models.user import User
from app.db.session import get_session

@pytest.mark.asyncio
async def test_microsoft_login_redirect():
    with patch("app.api.v1.routes_oauth.oauth") as mock_oauth:
        mock_oauth.microsoft.authorize_redirect.return_value = "Redirect Fake Response"
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            await ac.get("/api/v1/auth/microsoft/login")
        
        assert mock_oauth.microsoft.authorize_redirect.called

@pytest.mark.asyncio
async def test_microsoft_callback_success(test_session):
    mock_token = {"access_token": "fake_ms_token", "userinfo": {"email": "msuser@example.com", "sub": "ms_sub_123"}}
    
    with patch("app.api.v1.routes_oauth.oauth") as mock_oauth:
        # Userinfo on token fallback? logic: token.get("userinfo") OR oauth.microsoft.userinfo(token)
        # We mock authorize_access_token to return token with userinfo
        mock_oauth.microsoft.authorize_access_token = AsyncMock(return_value=mock_token)
        
        app.dependency_overrides[get_session] = lambda: test_session
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/api/v1/auth/microsoft/callback")
        
        assert response.status_code == 307
        assert "access_token" in response.headers["location"]
        
        # Verify DB
        from sqlmodel import select
        stmt = select(User).where(User.email == "msuser@example.com")
        result = await test_session.exec(stmt)
        user = result.first()
        assert user is not None
        assert user.auth_provider == "microsoft"

        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_github_login_redirect():
    with patch("app.api.v1.routes_oauth.oauth") as mock_oauth:
        mock_oauth.github.authorize_redirect.return_value = "Redirect Fake Response"
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            await ac.get("/api/v1/auth/github/login")
        
        assert mock_oauth.github.authorize_redirect.called

@pytest.mark.asyncio
async def test_github_callback_public_email(test_session):
    mock_token = {"access_token": "fake_gh_token"}
    mock_user_resp = MagicMock()
    mock_user_resp.json.return_value = {"email": "gh_public@example.com", "id": 12345}
    
    with patch("app.api.v1.routes_oauth.oauth") as mock_oauth:
        mock_oauth.github.authorize_access_token = AsyncMock(return_value=mock_token)
        mock_oauth.github.get = AsyncMock(return_value=mock_user_resp)
        
        app.dependency_overrides[get_session] = lambda: test_session
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/api/v1/auth/github/callback")
            
        assert response.status_code == 307
        assert "access_token" in response.headers["location"]
        
        # Verify DB
        from sqlmodel import select
        stmt = select(User).where(User.email == "gh_public@example.com")
        result = await test_session.exec(stmt)
        user = result.first()
        assert user is not None
        assert user.auth_provider == "github"
        
        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_github_callback_private_email(test_session):
    mock_token = {"access_token": "fake_gh_token"}
    
    mock_user_resp = MagicMock()
    mock_user_resp.json.return_value = {"email": None, "id": 67890}
    
    mock_emails_resp = MagicMock()
    mock_emails_resp.json.return_value = [
        {"email": "private@example.com", "primary": True, "verified": True},
        {"email": "other@example.com", "primary": False, "verified": True}
    ]
    
    with patch("app.api.v1.routes_oauth.oauth") as mock_oauth:
        mock_oauth.github.authorize_access_token = AsyncMock(return_value=mock_token)
        mock_oauth.github.get = AsyncMock(side_effect=[mock_user_resp, mock_emails_resp])
        
        app.dependency_overrides[get_session] = lambda: test_session
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/api/v1/auth/github/callback")
            
        assert response.status_code == 307
        
        # Verify DB
        from sqlmodel import select
        stmt = select(User).where(User.email == "private@example.com")
        result = await test_session.exec(stmt)
        user = result.first()
        assert user is not None
        assert user.auth_provider == "github"
        
        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_microsoft_callback_success(test_session):
    mock_token = {"access_token": "fake_ms_token", "userinfo": {"email": "msuser@example.com", "sub": "ms_sub_123"}}
    
    with patch("app.core.oauth.oauth") as mock_oauth:
        # Userinfo on token fallback? logic: token.get("userinfo") OR oauth.microsoft.userinfo(token)
        # We mock authorize_access_token to return token with userinfo
        mock_oauth.microsoft.authorize_access_token = AsyncMock(return_value=mock_token)
        
        app.dependency_overrides[get_session] = lambda: test_session
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/api/v1/auth/microsoft/callback")
        
        assert response.status_code == 307
        assert "access_token" in response.headers["location"]
        
        # Verify DB
        from sqlmodel import select
        stmt = select(User).where(User.email == "msuser@example.com")
        result = await test_session.exec(stmt)
        user = result.first()
        assert user is not None
        assert user.auth_provider == "microsoft"

        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_github_login_redirect():
    with patch("app.core.oauth.oauth") as mock_oauth:
        mock_oauth.github.authorize_redirect.return_value = "Redirect Fake Response"
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            await ac.get("/api/v1/auth/github/login")
        
        assert mock_oauth.github.authorize_redirect.called

@pytest.mark.asyncio
async def test_github_callback_public_email(test_session):
    mock_token = {"access_token": "fake_gh_token"}
    mock_user_resp = MagicMock()
    mock_user_resp.json.return_value = {"email": "gh_public@example.com", "id": 12345}
    
    with patch("app.core.oauth.oauth") as mock_oauth:
        mock_oauth.github.authorize_access_token = AsyncMock(return_value=mock_token)
        mock_oauth.github.get = AsyncMock(return_value=mock_user_resp)
        
        app.dependency_overrides[get_session] = lambda: test_session
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/api/v1/auth/github/callback")
            
        assert response.status_code == 307
        assert "access_token" in response.headers["location"]
        
        # Verify DB
        from sqlmodel import select
        stmt = select(User).where(User.email == "gh_public@example.com")
        result = await test_session.exec(stmt)
        user = result.first()
        assert user is not None
        assert user.auth_provider == "github"
        
        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_github_callback_private_email(test_session):
    mock_token = {"access_token": "fake_gh_token"}
    
    mock_user_resp = MagicMock()
    mock_user_resp.json.return_value = {"email": None, "id": 67890}
    
    mock_emails_resp = MagicMock()
    mock_emails_resp.json.return_value = [
        {"email": "private@example.com", "primary": True, "verified": True},
        {"email": "other@example.com", "primary": False, "verified": True}
    ]
    
    with patch("app.core.oauth.oauth") as mock_oauth:
        mock_oauth.github.authorize_access_token = AsyncMock(return_value=mock_token)
        mock_oauth.github.get = AsyncMock(side_effect=[mock_user_resp, mock_emails_resp])
        
        app.dependency_overrides[get_session] = lambda: test_session
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/api/v1/auth/github/callback")
            
        assert response.status_code == 307
        
        # Verify DB
        from sqlmodel import select
        stmt = select(User).where(User.email == "private@example.com")
        result = await test_session.exec(stmt)
        user = result.first()
        assert user is not None
        assert user.auth_provider == "github"
        
        app.dependency_overrides.clear()
@pytest.mark.asyncio
async def test_microsoft_login_redirect():
    with patch("app.api.v1.routes_oauth.oauth.microsoft.authorize_redirect") as mock_authorize:
        mock_authorize.return_value = "Redirect Fake Response"
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            await ac.get("/api/v1/auth/microsoft/login")
        
        assert mock_authorize.called

@pytest.mark.asyncio
async def test_microsoft_callback_success(test_session):
    mock_token = {"access_token": "fake_ms_token", "userinfo": {"email": "msuser@example.com", "sub": "ms_sub_123"}}
    
    with patch("app.api.v1.routes_oauth.oauth.microsoft.authorize_access_token", new_callable=AsyncMock) as mock_access_token:
        mock_access_token.return_value = mock_token
        
        app.dependency_overrides[get_session] = lambda: test_session
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/api/v1/auth/microsoft/callback")
        
        assert response.status_code == 307 # Redirects to frontend
        assert "access_token" in response.headers["location"]
        
        # Verify DB
        from sqlmodel import select
        stmt = select(User).where(User.email == "msuser@example.com")
        result = await test_session.exec(stmt)
        user = result.first()
        assert user is not None
        assert user.auth_provider == "microsoft"

        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_github_login_redirect():
    with patch("app.api.v1.routes_oauth.oauth.github.authorize_redirect") as mock_authorize:
        mock_authorize.return_value = "Redirect Fake Response"
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            await ac.get("/api/v1/auth/github/login")
        
        assert mock_authorize.called

@pytest.mark.asyncio
async def test_github_callback_public_email(test_session):
    # Mock token response + Get User response
    mock_token = {"access_token": "fake_gh_token"}
    mock_user_resp = AsyncMock()
    mock_user_resp.json.return_value = {"email": "gh_public@example.com", "id": 12345}
    
    with patch("app.api.v1.routes_oauth.oauth.github.authorize_access_token", new_callable=AsyncMock) as mock_access_token, \
         patch("app.api.v1.routes_oauth.oauth.github.get", new_callable=AsyncMock, create=True) as mock_get:
        
        mock_access_token.return_value = mock_token
        mock_get.return_value = mock_user_resp
        
        app.dependency_overrides[get_session] = lambda: test_session
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            try:
                response = await ac.get("/api/v1/auth/github/callback")
                assert response.status_code == 307
                assert "access_token" in response.headers["location"]
            except Exception as e:
                import traceback
                traceback.print_exc()
                raise e
        
        # Verify DB
        from sqlmodel import select
        stmt = select(User).where(User.email == "gh_public@example.com")
        result = await test_session.exec(stmt)
        user = result.first()
        assert user is not None
        assert user.auth_provider == "github"
        
        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_github_callback_private_email(test_session):
    # Mock token response + Get User response (no email) + Get Emails response
    mock_token = {"access_token": "fake_gh_token"}
    
    mock_user_resp = AsyncMock()
    mock_user_resp.json.return_value = {"email": None, "id": 67890}
    
    mock_emails_resp = AsyncMock()
    mock_emails_resp.json.return_value = [
        {"email": "private@example.com", "primary": True, "verified": True},
        {"email": "other@example.com", "primary": False, "verified": True}
    ]
    
    with patch("app.api.v1.routes_oauth.oauth.github.authorize_access_token", new_callable=AsyncMock) as mock_access_token, \
         patch("app.api.v1.routes_oauth.oauth.github.get", new_callable=AsyncMock, create=True) as mock_get:
        
        mock_access_token.return_value = mock_token
        # side_effect for multiple calls: first call user, second call emails
        mock_get.side_effect = [mock_user_resp, mock_emails_resp]
        
        app.dependency_overrides[get_session] = lambda: test_session
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/api/v1/auth/github/callback")
            
        assert response.status_code == 307
        
        # Verify DB
        from sqlmodel import select
        stmt = select(User).where(User.email == "private@example.com")
        result = await test_session.exec(stmt)
        user = result.first()
        assert user is not None
        assert user.auth_provider == "github"
        
        app.dependency_overrides.clear()
