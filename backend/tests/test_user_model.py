import pytest
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from sqlmodel import select

@pytest.mark.asyncio
async def test_create_user(test_session):
    """
    Test creating a new user (Async).
    """
    user_data = {
        "email": "test@example.com",
        "hashed_password": "hashed_secret",
        "auth_provider": "local"
    }
    user = User(**user_data)
    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)

    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.is_active is True

@pytest.mark.asyncio
async def test_retrieve_user(test_session):
    """
    Test retrieving an existing user (Async).
    """
    user = User(email="retrieve@example.com", auth_provider="local")
    test_session.add(user)
    await test_session.commit()

    statement = select(User).where(User.email == "retrieve@example.com")
    result = await test_session.exec(statement)
    retrieved_user = result.first()
    
    assert retrieved_user is not None
    assert retrieved_user.email == "retrieve@example.com"
    assert retrieved_user.id == user.id

@pytest.mark.asyncio
async def test_unique_email_constraint(test_session):
    """
    Test that identifying duplicate emails raises an IntegrityError.
    """
    user1 = User(email="unique@example.com", auth_provider="local")
    test_session.add(user1)
    await test_session.commit()

    user2 = User(email="unique@example.com", auth_provider="local")
    test_session.add(user2)
    
    with pytest.raises(IntegrityError):
        await test_session.commit()
    
    await test_session.rollback()
