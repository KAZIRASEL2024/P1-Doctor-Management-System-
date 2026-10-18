"""Alembic environment configuration for async SQLAlchemy."""
from __future__ import annotations

import asyncio
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

# Import models so Alembic can detect them
from app.db.base import Base
import app.models.user  # noqa: F401
import app.models.zone  # noqa: F401
import app.models.doctor  # noqa: F401
import app.models.doctor_zone_assignment  # noqa: F401
import app.models.consultation  # noqa: F401
import app.models.attachment  # noqa: F401
import app.models.consultation_response  # noqa: F401
import app.models.notification  # noqa: F401
import app.models.audit_log  # noqa: F401
import app.models.patient  # noqa: F401
import app.models.patient_profile  # noqa: F401
import app.models.medical_query  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# Override sqlalchemy.url with env var if present
db_url = os.environ.get("DATABASE_URL") or config.get_main_option("sqlalchemy.url")


def run_migrations_offline() -> None:
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):  # type: ignore[no-untyped-def]
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    engine = create_async_engine(db_url)
    async with engine.connect() as conn:
        await conn.run_sync(do_run_migrations)
    await engine.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
