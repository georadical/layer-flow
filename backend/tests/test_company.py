import pytest
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from app.models.user import User
from app.models.company import Company
from app.models.user_company import UserCompany

@pytest.mark.asyncio
async def test_create_company(test_session):
    """
    Test creating a company.
    """
    company = Company(name="Test Corp", plan_tier="free")
    test_session.add(company)
    await test_session.commit()
    await test_session.refresh(company)

    assert company.id is not None
    assert company.name == "Test Corp"
    assert company.plan_tier == "free"

@pytest.mark.asyncio
async def test_user_joins_company(test_session):
    """
    Test user joining a company with a specific role.
    """
    # Create User
    user = User(email="joiner@example.com", auth_provider="local")
    test_session.add(user)
    
    # Create Company
    company = Company(name="Join Corp")
    test_session.add(company)
    await test_session.commit()
    
    # Create Link
    link = UserCompany(user_id=user.id, company_id=company.id, role="admin")
    test_session.add(link)
    await test_session.commit()
    await test_session.refresh(link)
    
    # Verify link
    assert link.role == "admin"
    assert link.user_id == user.id
    assert link.company_id == company.id

    # Verify relationships (need refresh or loading)
    # Re-fetch user to see companies
    # Note: Async lazy loading isn't supported in standard SQLAlchemy/SQLModel the same way.
    # We must execute a query to fetch related items or use explicit loading options.
    # However, for this test, we can just query the link table or use select with joins.
    
    # Let's verify via relationship loading if possible, or direct query
    # Using selectinload is best practice for async relationships
    from sqlalchemy.orm import selectinload
    
    stmt = select(User).where(User.id == user.id).options(selectinload(User.companies))
    result = await test_session.exec(stmt)
    user_loaded = result.first()
    
    assert len(user_loaded.companies) == 1
    assert user_loaded.companies[0].company_id == company.id
    assert user_loaded.companies[0].role == "admin"

@pytest.mark.asyncio
async def test_duplicate_company_name(test_session):
    """
    Test that duplicate company names fail.
    """
    c1 = Company(name="Unique Corp")
    test_session.add(c1)
    await test_session.commit()

    c2 = Company(name="Unique Corp")
    test_session.add(c2)
    
    with pytest.raises(IntegrityError):
        await test_session.commit()
    
    await test_session.rollback()
