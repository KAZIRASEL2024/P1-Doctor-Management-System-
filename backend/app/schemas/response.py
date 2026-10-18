"""Doctor response schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class ResponseCreate(BaseModel):
    consultation_id: int
    diagnosis: str = Field(..., min_length=10)
    treatment_plan: str = Field(..., min_length=10)
    medications: str | None = None
    follow_up_instructions: str | None = None
    is_emergency_referral: bool = False


class ResponseOut(BaseModel):
    id: int
    consultation_id: int
    doctor_id: int
    diagnosis: str
    treatment_plan: str
    medications: str | None
    follow_up_instructions: str | None
    is_emergency_referral: bool

    model_config = {"from_attributes": True}
