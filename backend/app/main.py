"""FastAPI application entry point."""
from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from app.api.router import api_router
from app.api.routes.workflow import router as workflow_router
from app.core.config import settings
from app.core.exceptions import http_exception_handler
from app.core.logging import configure_logging, get_logger
from app.core.security import hash_password
from app.db.session import AsyncSessionLocal, engine
from app.models.user import User

log = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    configure_logging("DEBUG" if settings.ENVIRONMENT == "development" else "INFO")
    log.info("Starting BRAC AISP Doctor Management System", env=settings.ENVIRONMENT)

    if settings.ADMIN_EMAIL and settings.ADMIN_PASSWORD:
        if len(settings.ADMIN_PASSWORD) < 12:
            raise RuntimeError("ADMIN_PASSWORD must contain at least 12 characters.")
        async with AsyncSessionLocal() as db:
            configured_user = await db.scalar(
                select(User).where(
                    User.email == settings.ADMIN_EMAIL.strip().lower()
                )
            )
            if configured_user is None:
                db.add(
                    User(
                        email=settings.ADMIN_EMAIL.strip().lower(),
                        hashed_password=hash_password(settings.ADMIN_PASSWORD),
                        full_name="System Administrator",
                        role="admin",
                    )
                )
                await db.commit()
                log.info("Initial administrator account created")
            elif configured_user.role != "admin":
                raise RuntimeError(
                    "ADMIN_EMAIL is already registered to a non-administrator account."
                )

    if settings.SEED_DEMO_DATA:
        try:
            from scripts.seed_demo_data import seed  # type: ignore[import]
            from app.db.session import AsyncSessionLocal

            async with AsyncSessionLocal() as db:
                await seed(db)
            log.info("Demo data seeded successfully")
        except Exception as exc:
            log.warning("Demo data seeding skipped", reason=str(exc))

    yield
    log.info("Shutting down")
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Human Doctor Management System for patient queries and doctor responses.",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

app.include_router(workflow_router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)  # type: ignore[arg-type]

# Routes
app.include_router(api_router)
