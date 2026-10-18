"""Run database migrations, adopting an existing initial schema when needed."""
from __future__ import annotations

import asyncio
import subprocess
import sys
from pathlib import Path

from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings

INITIAL_TABLES = {
    "users",
    "zones",
    "doctors",
    "doctor_zone_assignments",
    "consultations",
    "attachments",
    "consultation_responses",
    "notifications",
    "audit_logs",
}


async def existing_tables() -> set[str]:
    engine = create_async_engine(settings.DATABASE_URL)
    try:
        async with engine.connect() as connection:
            return await connection.run_sync(
                lambda sync_connection: set(inspect(sync_connection).get_table_names())
            )
    finally:
        await engine.dispose()


def run_alembic(*arguments: str) -> None:
    backend_dir = Path(__file__).resolve().parent.parent
    subprocess.run(
        [sys.executable, "-m", "alembic", *arguments],
        cwd=backend_dir,
        check=True,
    )


async def main() -> None:
    tables = await existing_tables()
    if "alembic_version" not in tables and INITIAL_TABLES.issubset(tables):
        run_alembic("stamp", "0001_initial_schema")
    run_alembic("upgrade", "head")


if __name__ == "__main__":
    asyncio.run(main())
