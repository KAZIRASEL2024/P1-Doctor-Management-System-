"""Notification routes."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import current_user_dep
from app.db.session import get_db
from app.models.user import User
from app.schemas.notification import NotificationListResponse
from app.services import notification_service

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("", response_model=NotificationListResponse)
async def list_notifications(
    unread_only: bool = Query(False),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user_dep),
) -> NotificationListResponse:
    return await notification_service.list_notifications(db, current_user.id, unread_only)


@router.patch("/{notification_id}/read")
async def mark_read(
    notification_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user_dep),
) -> dict:
    await notification_service.mark_read(db, notification_id, current_user.id)
    return {"success": True}
