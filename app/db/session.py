import asyncio
from typing import AsyncGenerator

from sqlalchemy import create_engine, event
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import get_settings
from app.core.logging import setup_logging

logger = setup_logging()
settings = get_settings()

# Async Engine (for FastAPI)
async_engine: AsyncEngine = create_async_engine(
    settings.postgres_async_url,
    echo=settings.debug,
    pool_size=settings.postgres_pool_size,
    max_overflow=settings.postgres_max_overflow,
    pool_timeout=settings.postgres_pool_timeout,
    pool_recycle=settings.postgres_pool_recycle,
    pool_pre_ping=True,
    connect_args={
        "server_settings": {
            "application_name": f"{settings.app_name}_async",
        },
    },
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


# Sync Engine (for Celery & Alembic)
sync_engine = create_engine(
    settings.postgres_sync_url,
    echo=settings.debug,
    pool_size=settings.postgres_pool_size,
    max_overflow=settings.postgres_max_overflow,
    pool_timeout=settings.postgres_pool_timeout,
    pool_recycle=settings.postgres_pool_recycle,
    pool_pre_ping=True,
    connect_args={
        "application_name": f"{settings.app_name}_sync",
    },
)

# Sync session factory
SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


# Session Dependencies
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency for async database sessions.
    
    Usage:
        @router.get("/users")
        async def get_users(db: AsyncSession = Depends(get_async_session)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def get_sync_session() -> Session:
    """
    Get sync session for Celery tasks.
    
    Usage (in Celery task):
        db = get_sync_session()
        try:
            # Your database operations
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
    """
    return SyncSessionLocal()


# Database Initialization
async def init_db(retries: int = 10, delay: int = 2) -> None:
    """
    Initialize database connection with retry logic.
    Useful for waiting for PostgreSQL to be ready in Docker.
    """
    from app.models.base import Base
    
    for attempt in range(1, retries + 1):
        try:
            async with async_engine.begin() as conn:
                # Create all tables (in production, use Alembic migrations instead)
                if settings.debug:
                    await conn.run_sync(Base.metadata.create_all)
                
                # Test connection
                await conn.execute("SELECT 1")
                
            logger.info("✓ Database connection established successfully")
            return
            
        except Exception as e:
            logger.warning(
                f"Database connection attempt {attempt}/{retries} failed: {e}"
            )
            if attempt < retries:
                await asyncio.sleep(delay)
            else:
                logger.error("Failed to connect to database after all retries")
                raise RuntimeError(
                    "Database initialization failed after maximum retries"
                ) from e


async def close_db() -> None:
    """Close database connections gracefully"""
    try:
        await async_engine.dispose()
        logger.info("✓ Async database connections closed")
    except Exception as e:
        logger.error(f"Error closing async database connections: {e}")
    
    try:
        sync_engine.dispose()
        logger.info("✓ Sync database connections closed")
    except Exception as e:
        logger.error(f"Error closing sync database connections: {e}")


# Event Listeners (Optional)
@event.listens_for(sync_engine, "connect")
def receive_connect(dbapi_conn, connection_record):
    """Set connection-level settings on connect"""
    # Example: Set statement timeout
    # cursor = dbapi_conn.cursor()
    # cursor.execute("SET statement_timeout = '30s'")
    # cursor.close()
    pass


@event.listens_for(sync_engine, "checkout")
def receive_checkout(dbapi_conn, connection_record, connection_proxy):
    """Validate connection on checkout"""
    # Connection validation is handled by pool_pre_ping=True
    pass