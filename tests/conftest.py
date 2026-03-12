"""
Pytest configuration and fixtures for TeacherManager tests.

Provides:
- TestClient for FastAPI app
- Async test database session (in-memory SQLite)
- Fixtures for authenticated users, students, etc.
"""

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import event
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.main import app
from app.core.database import get_session
from app.models import Base


# ============ Database Fixtures ============
@pytest.fixture(scope="function")
async def test_db_engine():
    """Create in-memory SQLite test database engine.
    
    Uses StaticPool to avoid SQLite "database is locked" errors in async tests.
    Creates fresh schema for each test.
    """
    # Create in-memory SQLite engine for testing
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def test_db_session(test_db_engine):
    """Create test database session.
    
    Provides an async session connected to the in-memory test database.
    Automatically rolls back after each test.
    """
    async_session_maker = async_sessionmaker(
        test_db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    async with async_session_maker() as session:
        # Start transaction to enable rollback
        async with session.begin_nested():
            yield session


@pytest.fixture
def override_get_db(test_db_session):
    """Override get_session dependency for tests.
    
    Allows FastAPI routes to use test database session.
    """
    async def get_test_db():
        yield test_db_session

    app.dependency_overrides[get_session] = get_test_db
    yield
    del app.dependency_overrides[get_session]


# ============ Client Fixtures ============
@pytest.fixture
def client(override_get_db):
    """Create TestClient for synchronous tests.
    
    Usage:
        def test_health_check(client):
            response = client.get("/health")
            assert response.status_code == 200
    """
    return TestClient(app)


@pytest.fixture
async def async_client(override_get_db):
    """Create AsyncClient for async/await tests.
    
    Usage:
        async def test_async_endpoint(async_client):
            response = await async_client.get("/api/v1/students")
            assert response.status_code in [200, 501]  # 501 while stubs
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


# ============ Pytest Configuration ============
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test (requires DB)"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test (no DB)"
    )
