"""Consultation routes."""
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import current_user_dep
from app.db.session import get_db
from app.models.user import User
from app.schemas.consultation import ConsultationDetail, ConsultationListResponse
from app.services import consultation_service

router = APIRouter(prefix="/consultations", tags=["Consultations"])


@router.get("", response_model=ConsultationListResponse)
async def list_consultations(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    zone_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(current_user_dep),
) -> ConsultationListResponse:
    return await consultation_service.list_consultations(
        db,
        page=page,
        page_size=page_size,
        status=status,
        priority=priority,
        zone_id=zone_id,
        search=search,
    )


@router.get("/{consultation_id}", response_model=ConsultationDetail)
async def get_consultation(
    consultation_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(current_user_dep),
) -> ConsultationDetail:
    return await consultation_service.get_consultation(db, consultation_id)
