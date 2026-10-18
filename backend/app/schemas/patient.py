"""Patient schemas."""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class PatientCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    species: str = Field(min_length=1, max_length=100)
    breed: Optional[str] = Field(default=None, max_length=100)
    sex: Optional[str] = Field(default=None, max_length=30)
    age_months: Optional[int] = Field(default=None, ge=0)
    weight_kg: Optional[float] = Field(default=None, gt=0)
    owner_name: str = Field(min_length=1, max_length=255)
    owner_phone: Optional[str] = Field(default=None, max_length=30)
    location: Optional[str] = Field(default=None, max_length=255)
    medical_notes: Optional[str] = None


class PatientOut(PatientCreate):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class PatientListResponse(BaseModel):
    items: List[PatientOut]
    total: int
