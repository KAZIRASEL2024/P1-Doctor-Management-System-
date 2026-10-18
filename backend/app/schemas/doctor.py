"""Doctor schemas."""
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class DoctorCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    registration_number: str = Field(min_length=1, max_length=100)
    specialization: str = Field(min_length=1, max_length=255)
    qualification: str = Field(min_length=1, max_length=255)
    phone: str = Field(min_length=1, max_length=30)
    bio: Optional[str] = None
    is_emergency_doctor: bool = False
    is_available: bool = True
    zone_ids: List[int] = Field(default_factory=list)


class ZoneBrief(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class DoctorListItem(BaseModel):
    id: int
    user_id: int
    full_name: str
    email: str
    registration_number: str
    specialization: str
    qualification: str
    phone: str
    is_emergency_doctor: bool
    is_available: bool
    zones: List[ZoneBrief] = []
    total_responses: int = 0

    model_config = {"from_attributes": True}


class DoctorDetail(DoctorListItem):
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

    model_config = {"from_attributes": True}


class DoctorListResponse(BaseModel):
    items: List[DoctorListItem]
    total: int
