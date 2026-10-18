"""Schemas for the human patient/doctor workflow."""
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class PatientRegistration(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    name: str = Field(min_length=1, max_length=255)
    age: int = Field(ge=0, le=130)
    gender: str = Field(min_length=1, max_length=50)
    contact_details: str = Field(min_length=1, max_length=255)


class DoctorCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    specialization: str = Field(min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    phone: str | None = Field(default=None, max_length=30)


class DoctorSummary(BaseModel):
    id: int
    name: str
    specialization: str
    email: EmailStr
    phone: str | None = None


class AdminStats(BaseModel):
    total_doctors: int
    total_patients: int
    total_queries: int
    pending_queries: int
    answered_queries: int


class MedicalQueryCreate(BaseModel):
    doctor_id: int
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1, max_length=10000)


class MedicalAnswer(BaseModel):
    answer: str = Field(min_length=1, max_length=10000)


class MedicalQueryOut(BaseModel):
    id: int
    patient_id: int
    patient_name: str
    doctor_id: int
    doctor_name: str
    title: str
    description: str
    answer: str | None
    status: str
    created_at: datetime
    updated_at: datetime


class PatientRegistrationOut(BaseModel):
    id: int
    email: EmailStr
    name: str
