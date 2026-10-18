"""Consultation Pydantic schemas."""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class AttachmentOut(BaseModel):
    id: int
    file_name: str
    file_type: str
    mime_type: str
    storage_path: str
    file_size_bytes: int
    uploaded_at: datetime

    model_config = {"from_attributes": True}


class ConsultationResponseOut(BaseModel):
    id: int
    doctor_id: int
    diagnosis: str
    treatment_plan: str
    medications: Optional[str] = None
    follow_up_instructions: Optional[str] = None
    is_emergency_referral: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ConsultationListItem(BaseModel):
    id: int
    aisp_reference: Optional[str] = None
    zone_id: Optional[int] = None
    zone_name: Optional[str] = None
    field_worker_name: str
    animal_species: str
    animal_breed: Optional[str] = None
    symptoms: str
    priority: str
    status: str
    submitted_at: datetime
    sla_deadline: Optional[datetime] = None
    responded_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ConsultationDetail(ConsultationListItem):
    field_worker_phone: Optional[str] = None
    animal_age_months: Optional[int] = None
    animal_weight_kg: Optional[float] = None
    animal_temperature_celsius: Optional[float] = None
    animal_owner_name: Optional[str] = None
    remarks: Optional[str] = None
    closed_at: Optional[datetime] = None
    attachments: List[AttachmentOut] = []
    responses: List[ConsultationResponseOut] = []

    model_config = {"from_attributes": True}


class ConsultationListResponse(BaseModel):
    items: List[ConsultationListItem]
    total: int
    page: int
    page_size: int
    total_pages: int
