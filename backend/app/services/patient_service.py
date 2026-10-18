"""Patient list, create, and detail operations."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientListResponse, PatientOut


async def list_patients(db: AsyncSession) -> PatientListResponse:
    result = await db.execute(
        select(Patient).order_by(Patient.created_at.desc(), Patient.id.desc())
    )
    patients = result.scalars().all()
    return PatientListResponse(
        items=[PatientOut.model_validate(patient) for patient in patients],
        total=len(patients),
    )


async def create_patient(db: AsyncSession, body: PatientCreate) -> PatientOut:
    patient = Patient(**body.model_dump())
    db.add(patient)
    await db.commit()
    await db.refresh(patient)
    return PatientOut.model_validate(patient)


async def get_patient(db: AsyncSession, patient_id: int) -> PatientOut:
    patient = await db.get(Patient, patient_id)
    if patient is None:
        raise NotFoundError(f"Patient {patient_id} not found.")
    return PatientOut.model_validate(patient)
