"""Dashboard routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import current_user_dep
from app.db.session import get_db
from app.models.user import User
from app.schemas.dashboard import DashboardStats
from app.services import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=DashboardStats)
async def get_stats(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(current_user_dep),
) -> DashboardStats:
    return await dashboard_service.get_dashboard_stats(db)
