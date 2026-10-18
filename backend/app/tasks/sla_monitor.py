"""
SLA Monitor — background task that marks consultations as overdue.

STATUS: STUB (not hooked into a scheduler yet)

To activate: integrate with APScheduler or Celery Beat and call
`check_sla()` on a recurring schedule (e.g., every 5 minutes).
"""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.consultation import Consultation
from app.models.notification import Notification
from app.core.logging import get_logger

log = get_logger(__name__)


async def check_sla(db: AsyncSession) -> int:
    """
    Find all consultations past their SLA deadline that are not yet responded.
    Mark them as 'overdue' and create notifications.

    Returns the number of cases newly marked overdue.
    """
    now = datetime.now(timezone.utc)

    result = await db.execute(
        select(Consultation).where(
            Consultation.sla_deadline < now,
            Consultation.status.in_(["pending", "in_progress"]),
        )
    )
    cases = result.scalars().all()

    marked = 0
    for case in cases:
        case.status = "overdue"

        # Create notification for the assigned doctor (simplified: notify all)
        # TODO: look up assigned doctor by zone and create targeted notification
        log.warning("Consultation overdue", consultation_id=case.id, ref=case.aisp_reference)
        marked += 1

    if marked:
        await db.commit()
        log.info("SLA check complete", newly_overdue=marked)

    return marked
