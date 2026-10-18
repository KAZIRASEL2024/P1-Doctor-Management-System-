"""Doctor routes."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import current_user_dep
from app.core.permissions import require_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.doctor import DoctorCreate, DoctorDetail, DoctorListResponse
from app.services import doctor_service

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.post("", response_model=DoctorDetail, status_code=status.HTTP_201_CREATED)
async def create_doctor(
    body: DoctorCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user_dep),
) -> DoctorDetail:
    require_admin(current_user)
    return await doctor_service.create_doctor(db, body)


@router.get("", response_model=DoctorListResponse)
async def list_doctors(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(current_user_dep),
) -> DoctorListResponse:
    return await doctor_service.list_doctors(db)


@router.get("/{doctor_id}", response_model=DoctorDetail)
async def get_doctor(
    doctor_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(current_user_dep),
) -> DoctorDetail:
    return await doctor_service.get_doctor(db, doctor_id)
