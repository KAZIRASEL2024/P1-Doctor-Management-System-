"""Health check endpoint."""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


@router.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check() -> HealthResponse:
    """Returns OK when the service is running."""
    return HealthResponse(
        status="ok",
        service="BRAC AISP Doctor Management System",
        version="1.0.0",
    )
