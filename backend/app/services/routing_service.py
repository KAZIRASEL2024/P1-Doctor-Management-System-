"""
Emergency routing service.

Routes after-hours consultations to the designated Emergency Doctor.
STATUS: Configured but not yet hooked into consultation creation flow.
"""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logging import get_logger
from app.models.doctor import Doctor

log = get_logger(__name__)


def is_operating_hours(dt: datetime | None = None) -> bool:
    """Return True if the current time is within configured operating hours."""
    now = dt or datetime.now(timezone.utc)
    # Convert to Bangladesh time (UTC+6)
    bd_hour = (now.hour + 6) % 24
    return settings.OPERATING_HOUR_START <= bd_hour < settings.OPERATING_HOUR_END


async def get_emergency_doctor(db: AsyncSession) -> Doctor | None:
    """Return the first available emergency doctor."""
    result = await db.execute(
        select(Doctor).where(
            Doctor.is_emergency_doctor == True,
            Doctor.is_available == True,
        ).limit(1)
    )
    return result.scalar_one_or_none()


async def route_consultation(
    db: AsyncSession,
    zone_id: int | None,
    priority: str,
    submission_time: datetime | None = None,
) -> int | None:
    """
    Determine which doctor should handle a consultation.

    Returns the doctor_id to assign, or None if no suitable doctor found.
    Outside operating hours and for emergency cases, always routes to the
    emergency doctor.
    """
    is_emergency = priority == "emergency"
    after_hours  = not is_operating_hours(submission_time)

    if is_emergency or after_hours:
        emergency_doc = await get_emergency_doctor(db)
        if emergency_doc:
            log.info(
                "Routing to emergency doctor",
                doctor_id=emergency_doc.id,
                reason="emergency" if is_emergency else "after_hours",
            )
            return emergency_doc.id
        log.warning("No emergency doctor available")
        return None

    # Normal hours: route to a doctor assigned to the zone
    # TODO: implement weighted load-balancing across zone doctors
    return None
