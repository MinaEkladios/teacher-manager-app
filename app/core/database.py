"""
Database connection and session management.

Uses async SQLAlchemy with asyncpg for PostgreSQL.
Provides:
- Async engine and session factory
- Dependency injection for DB sessions in routes
- Lifecycle management (startup/shutdown)
"""

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.pool import NullPool
from typing import AsyncGenerator

from app.core.config import settings

# Create async engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,  # Log SQL statements in dev
    future=True,
    pool_size=20,
    max_overflow=40,
    poolclass=NullPool if settings.is_production else None,  # No connection pooling in prod (use external PgBouncer)
)

# Create async session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency: Get async database session.
    
    Usage in routes:
        @app.get("/items")
        async def get_items(session: AsyncSession = Depends(get_session)):
            result = await session.execute(select(Item))
            return result.scalars().all()
    
    Yields:
        AsyncSession: Async database session.
    """
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db() -> None:
    """Initialize database on startup.
    
    Called from app lifespan context manager.
    """
    # Check connection
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: None)  # Simple connection test
    print("✓ Database connection established")


async def close_db() -> None:
    """Close database on shutdown.
    
    Called from app lifespan context manager.
    """
    await engine.dispose()
    print("✓ Database connection closed")
