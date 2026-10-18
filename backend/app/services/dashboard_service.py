"""Dashboard statistics service."""
from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.consultation import Consultation
from app.models.doctor import Doctor
from app.models.zone import Zone
from app.schemas.dashboard import DashboardStats


async def get_dashboard_stats(db: AsyncSession) -> DashboardStats:
    # Consultation counts by status
    result = await db.execute(
        select(Consultation.status, func.count(Consultation.id)).group_by(Consultation.status)
    )
    status_counts = dict(result.all())

    total = sum(status_counts.values())
    pending = status_counts.get("pending", 0)
    in_progress = status_counts.get("in_progress", 0)
    responded = status_counts.get("responded", 0)
    overdue = status_counts.get("overdue", 0)

    # Doctor count
    doc_result = await db.execute(select(func.count(Doctor.id)))
    total_doctors = doc_result.scalar_one()

    # Active zone count
    zone_result = await db.execute(
        select(func.count(Zone.id)).where(Zone.is_active == True)
    )
    active_zones = zone_result.scalar_one()

    return DashboardStats(
        total_consultations=total,
        pending_consultations=pending,
        in_progress_consultations=in_progress,
        responded_consultations=responded,
        overdue_consultations=overdue,
        total_doctors=total_doctors,
        active_zones=active_zones,
        avg_response_time_minutes=None,  # TODO: calculate from responded consultations
    )
