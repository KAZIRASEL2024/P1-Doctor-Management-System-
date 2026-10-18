"""Zone list service."""
from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.consultation import Consultation
from app.models.doctor_zone_assignment import DoctorZoneAssignment
from app.models.zone import Zone
from app.schemas.zone import ZoneListResponse, ZoneOut


async def list_zones(db: AsyncSession) -> ZoneListResponse:
    result = await db.execute(select(Zone).order_by(Zone.name))
    zones = result.scalars().all()

    items = []
    for z in zones:
        doc_result = await db.execute(
            select(func.count(DoctorZoneAssignment.id)).where(
                DoctorZoneAssignment.zone_id == z.id
            )
        )
        doc_count = doc_result.scalar_one()

        c_result = await db.execute(
            select(func.count(Consultation.id)).where(Consultation.zone_id == z.id)
        )
        c_count = c_result.scalar_one()

        items.append(
            ZoneOut(
                id=z.id,
                name=z.name,
                erp_region_code=z.erp_region_code,
                description=z.description,
                is_active=z.is_active,
                doctor_count=doc_count,
                consultation_count=c_count,
            )
        )
    return ZoneListResponse(items=items, total=len(items))
