"""Zone schemas."""
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class ZoneOut(BaseModel):
    id: int
    name: str
    erp_region_code: Optional[str] = None
    description: Optional[str] = None
    is_active: bool
    doctor_count: int = 0
    consultation_count: int = 0

    model_config = {"from_attributes": True}


class ZoneListResponse(BaseModel):
    items: List[ZoneOut]
    total: int
