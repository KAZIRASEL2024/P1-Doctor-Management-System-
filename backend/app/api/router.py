"""Central API router — mounts all sub-routers."""
from fastapi import APIRouter

from app.api.routes import (
    auth,
    consultations,
    dashboard,
    doctors,
    health,
    notifications,
    patients,
    responses,
    zones,
)

api_router = APIRouter(prefix="/api")

api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(dashboard.router)
api_router.include_router(consultations.router)
api_router.include_router(responses.router)
api_router.include_router(doctors.router)
api_router.include_router(patients.router)
api_router.include_router(zones.router)
api_router.include_router(notifications.router)
