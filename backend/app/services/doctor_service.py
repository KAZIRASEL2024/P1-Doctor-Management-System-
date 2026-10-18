"""Doctor list/detail service."""
from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import ConflictError, NotFoundError, ValidationError
from app.core.security import hash_password
from app.models.consultation_response import ConsultationResponse
from app.models.doctor import Doctor
from app.models.doctor_zone_assignment import DoctorZoneAssignment
from app.models.user import User
from app.models.zone import Zone
from app.schemas.doctor import (
    DoctorCreate,
    DoctorDetail,
    DoctorListItem,
    DoctorListResponse,
    ZoneBrief,
)


def _build_list_item(doctor: Doctor, user: User, response_count: int) -> DoctorListItem:
    return DoctorListItem(
        id=doctor.id,
        user_id=doctor.user_id,
        full_name=user.full_name,
        email=user.email,
        registration_number=doctor.registration_number,
        specialization=doctor.specialization,
        qualification=doctor.qualification,
        phone=doctor.phone,
        is_emergency_doctor=doctor.is_emergency_doctor,
        is_available=doctor.is_available,
        zones=[
            ZoneBrief(id=a.zone.id, name=a.zone.name)
            for a in doctor.zone_assignments
            if a.zone
        ],
        total_responses=response_count,
    )


async def create_doctor(db: AsyncSession, body: DoctorCreate) -> DoctorDetail:
    existing_user = await db.execute(select(User).where(User.email == body.email))
    if existing_user.scalar_one_or_none() is not None:
        raise ConflictError("A user with this email address already exists.")

    existing_doctor = await db.execute(
        select(Doctor).where(Doctor.registration_number == body.registration_number)
    )
    if existing_doctor.scalar_one_or_none() is not None:
        raise ConflictError("A doctor with this registration number already exists.")

    zones_result = await db.execute(select(Zone).where(Zone.id.in_(body.zone_ids)))
    zones = zones_result.scalars().all()
    if len(zones) != len(set(body.zone_ids)):
        raise ValidationError("One or more selected zones do not exist.")

    user = User(
        email=str(body.email),
        hashed_password=hash_password(body.password),
        full_name=body.full_name,
        role="doctor",
    )
    db.add(user)
    await db.flush()

    doctor = Doctor(
        user_id=user.id,
        registration_number=body.registration_number,
        specialization=body.specialization,
        qualification=body.qualification,
        phone=body.phone,
        bio=body.bio,
        is_emergency_doctor=body.is_emergency_doctor,
        is_available=body.is_available,
    )
    db.add(doctor)
    await db.flush()

    db.add_all(
        DoctorZoneAssignment(doctor_id=doctor.id, zone_id=zone.id)
        for zone in zones
    )
    await db.commit()
    return await get_doctor(db, doctor.id)


async def list_doctors(db: AsyncSession) -> DoctorListResponse:
    result = await db.execute(
        select(Doctor)
        .options(
            selectinload(Doctor.user),
            selectinload(Doctor.zone_assignments).selectinload(DoctorZoneAssignment.zone),
        )
    )
    doctors = result.scalars().all()

    items = []
    for doc in doctors:
        # Count responses
        cnt_result = await db.execute(
            select(func.count(ConsultationResponse.id)).where(
                ConsultationResponse.doctor_id == doc.id
            )
        )
        rc = cnt_result.scalar_one()
        items.append(_build_list_item(doc, doc.user, rc))

    return DoctorListResponse(items=items, total=len(items))


async def get_doctor(db: AsyncSession, doctor_id: int) -> DoctorDetail:
    result = await db.execute(
        select(Doctor)
        .where(Doctor.id == doctor_id)
        .options(
            selectinload(Doctor.user),
            selectinload(Doctor.zone_assignments).selectinload(DoctorZoneAssignment.zone),
        )
    )
    doc = result.scalar_one_or_none()
    if doc is None:
        raise NotFoundError(f"Doctor {doctor_id} not found.")

    cnt_result = await db.execute(
        select(func.count(ConsultationResponse.id)).where(
            ConsultationResponse.doctor_id == doctor_id
        )
    )
    rc = cnt_result.scalar_one()

    base = _build_list_item(doc, doc.user, rc)
    return DoctorDetail(**base.model_dump(), bio=doc.bio, avatar_url=doc.avatar_url)
