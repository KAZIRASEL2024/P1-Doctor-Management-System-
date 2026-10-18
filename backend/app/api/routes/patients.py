"""Patient routes."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import current_user_dep
from app.db.session import get_db
from app.models.user import User
from app.schemas.patient import PatientCreate, PatientListResponse, PatientOut
from app.services import patient_service

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.get("", response_model=PatientListResponse)
async def list_patients(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(current_user_dep),
) -> PatientListResponse:
    return await patient_service.list_patients(db)


@router.post("", response_model=PatientOut, status_code=status.HTTP_201_CREATED)
async def create_patient(
    body: PatientCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(current_user_dep),
) -> PatientOut:
    return await patient_service.create_patient(db, body)


@router.get("/{patient_id}", response_model=PatientOut)
async def get_patient(
    patient_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(current_user_dep),
) -> PatientOut:
    return await patient_service.get_patient(db, patient_id)
