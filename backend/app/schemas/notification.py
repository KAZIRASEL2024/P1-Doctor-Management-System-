"""Notification schemas."""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class NotificationOut(BaseModel):
    id: int
    consultation_id: Optional[int] = None
    title: str
    body: str
    notification_type: str
    is_read: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class NotificationListResponse(BaseModel):
    items: List[NotificationOut]
    total: int
    unread_count: int
