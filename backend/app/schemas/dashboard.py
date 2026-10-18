"""Dashboard summary schema."""
from __future__ import annotations

from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_consultations: int
    pending_consultations: int
    in_progress_consultations: int
    responded_consultations: int
    overdue_consultations: int
    total_doctors: int
    active_zones: int
    avg_response_time_minutes: float | None = None
