"""pytest configuration and fixtures for backend tests."""
from __future__ import annotations

import asyncio
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.base import Base
from app.db.session import get_db
from app.main import app as fastapi_app   # avoid shadowing the 'app' package

# Import ALL models so SQLAlchemy can resolve relationships
import app.models.user                  # noqa: F401
import app.models.zone                  # noqa: F401
import app.models.doctor                # noqa: F401
import app.models.doctor_zone_assignment  # noqa: F401
import app.models.consultation          # noqa: F401
import app.models.attachment            # noqa: F401
import app.models.consultation_response # noqa: F401
import app.models.notification          # noqa: F401
import app.models.audit_log             # noqa: F401
import app.models.patient               # noqa: F401

# Use an in-memory SQLite database for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with session_factory() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession):
    async def override_get_db():
        yield db_session

    fastapi_app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    fastapi_app.dependency_overrides.clear()
