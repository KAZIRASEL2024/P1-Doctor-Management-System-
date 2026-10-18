"""Zone routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import current_user_dep
from app.db.session import get_db
from app.models.user import User
from app.schemas.zone import ZoneListResponse
from app.services.doctor_service_zone import list_zones

router = APIRouter(prefix="/zones", tags=["Zones"])


@router.get("", response_model=ZoneListResponse)
async def get_zones(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(current_user_dep),
) -> ZoneListResponse:
    return await list_zones(db)
