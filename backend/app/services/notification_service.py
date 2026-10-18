"""Notification service."""
from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import Notification
from app.schemas.notification import NotificationListResponse, NotificationOut


async def list_notifications(
    db: AsyncSession, user_id: int, unread_only: bool = False
) -> NotificationListResponse:
    query = select(Notification).where(Notification.user_id == user_id).order_by(
        Notification.created_at.desc()
    )
    if unread_only:
        query = query.where(Notification.is_read == False)

    result = await db.execute(query)
    rows = result.scalars().all()

    unread_result = await db.execute(
        select(func.count(Notification.id)).where(
            Notification.user_id == user_id, Notification.is_read == False
        )
    )
    unread = unread_result.scalar_one()

    return NotificationListResponse(
        items=[NotificationOut.model_validate(n) for n in rows],
        total=len(rows),
        unread_count=unread,
    )


async def mark_read(db: AsyncSession, notification_id: int, user_id: int) -> None:
    from datetime import datetime, timezone

    result = await db.execute(
        select(Notification).where(
            Notification.id == notification_id, Notification.user_id == user_id
        )
    )
    n = result.scalar_one_or_none()
    if n:
        n.is_read = True
        n.read_at = datetime.now(timezone.utc)
        await db.commit()
