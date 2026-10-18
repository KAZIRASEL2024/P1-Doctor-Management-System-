"""Human patient/doctor query workflow API."""
from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import current_user_dep
from app.core.exceptions import ConflictError, ForbiddenError, NotFoundError
from app.core.security import hash_password
from app.db.session import get_db
from app.models.doctor import Doctor
from app.models.medical_query import MedicalQuery
from app.models.patient_profile import PatientProfile
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.workflow import (
    DoctorCreateRequest,
    DoctorSummary,
    AdminStats,
    MedicalAnswer,
    MedicalQueryCreate,
    MedicalQueryOut,
    PatientRegistration,
    PatientRegistrationOut,
)
from app.services.auth_service import authenticate_user, issue_token

router = APIRouter(prefix="/api/v1")
auth_router = APIRouter(prefix="/auth", tags=["Auth v1"])
admin_router = APIRouter(prefix="/admin", tags=["Admin"])
patient_router = APIRouter(prefix="/patient", tags=["Patient"])
doctor_router = APIRouter(prefix="/doctor", tags=["Doctor"])


@auth_router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    """JSON login; use /token for OAuth2 password-form clients."""
    return TokenResponse(**issue_token(await authenticate_user(db, body.email, body.password)))


@auth_router.post("/token", response_model=TokenResponse)
async def oauth_token(
    credentials: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    return TokenResponse(
        **issue_token(
            await authenticate_user(db, credentials.username, credentials.password)
        )
    )


@admin_router.post("/doctors", response_model=DoctorSummary, status_code=status.HTTP_201_CREATED)
async def create_doctor(
    body: DoctorCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user_dep),
) -> DoctorSummary:
    _require_role(current_user, "admin")
    email = str(body.email).lower()
    existing = await db.scalar(select(User.id).where(User.email == email))
    if existing is not None:
        raise ConflictError("A user with this email address already exists.")

    user = User(
        email=email,
        hashed_password=hash_password(body.password),
        full_name=body.name.strip(),
        role="doctor",
    )
    db.add(user)
    await db.flush()
    doctor = Doctor(
        user_id=user.id,
        registration_number=f"DMS-{uuid4().hex[:16]}",
        specialization=body.specialization.strip(),
        qualification="Not specified",
        phone=body.phone or "",
    )
    db.add(doctor)
    await db.commit()
    return DoctorSummary(
        id=doctor.id,
        name=user.full_name,
        specialization=doctor.specialization,
        email=user.email,
        phone=doctor.phone or None,
    )


@admin_router.get("/doctors", response_model=list[DoctorSummary])
async def list_doctors(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user_dep),
) -> list[DoctorSummary]:
    _require_role(current_user, "admin")
    return await _list_doctors(db)


@admin_router.get("/stats", response_model=AdminStats)
async def admin_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user_dep),
) -> AdminStats:
    _require_role(current_user, "admin")
    total_doctors = await db.scalar(select(func.count(Doctor.id))) or 0
    total_patients = await db.scalar(select(func.count(PatientProfile.id))) or 0
    total_queries = await db.scalar(select(func.count(MedicalQuery.id))) or 0
    pending_queries = await db.scalar(
        select(func.count(MedicalQuery.id)).where(MedicalQuery.status == "Pending")
    ) or 0
    answered_queries = await db.scalar(
        select(func.count(MedicalQuery.id)).where(MedicalQuery.status == "Answered")
    ) or 0
    return AdminStats(
        total_doctors=total_doctors,
        total_patients=total_patients,
        total_queries=total_queries,
        pending_queries=pending_queries,
        answered_queries=answered_queries,
    )


@patient_router.post(
    "/register", response_model=PatientRegistrationOut, status_code=status.HTTP_201_CREATED
)
async def register_patient(
    body: PatientRegistration, db: AsyncSession = Depends(get_db)
) -> PatientRegistrationOut:
    email = str(body.email).lower()
    existing = await db.scalar(select(User.id).where(User.email == email))
    if existing is not None:
        raise ConflictError("An account with this email address already exists.")
    user = User(
        email=email,
        hashed_password=hash_password(body.password),
        full_name=body.name.strip(),
        role="patient",
    )
    db.add(user)
    await db.flush()
    patient = PatientProfile(
        user_id=user.id,
        name=body.name.strip(),
        age=body.age,
        gender=body.gender.strip(),
        contact_details=body.contact_details.strip(),
    )
    db.add(patient)
    await db.commit()
    return PatientRegistrationOut(id=patient.id, email=user.email, name=patient.name)


@patient_router.get("/doctors", response_model=list[DoctorSummary])
async def patient_doctors(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user_dep),
) -> list[DoctorSummary]:
    _require_role(current_user, "patient")
    return await _list_doctors(db)


@patient_router.post(
    "/queries", response_model=MedicalQueryOut, status_code=status.HTTP_201_CREATED
)
async def create_query(
    body: MedicalQueryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user_dep),
) -> MedicalQueryOut:
    _require_role(current_user, "patient")
    patient = await db.scalar(
        select(PatientProfile).where(PatientProfile.user_id == current_user.id)
    )
    if patient is None:
        raise NotFoundError("Patient profile not found.")
    doctor = await db.scalar(select(Doctor).where(Doctor.id == body.doctor_id))
    if doctor is None:
        raise NotFoundError("Doctor not found.")
    query = MedicalQuery(
        patient_id=patient.id,
        doctor_id=doctor.id,
        title=body.title.strip(),
        description=body.description.strip(),
        status="Pending",
    )
    db.add(query)
    await db.commit()
    return await _query_out(db, query)


@patient_router.get("/queries", response_model=list[MedicalQueryOut])
async def patient_queries(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user_dep),
) -> list[MedicalQueryOut]:
    _require_role(current_user, "patient")
    patient = await db.scalar(
        select(PatientProfile).where(PatientProfile.user_id == current_user.id)
    )
    if patient is None:
        raise NotFoundError("Patient profile not found.")
    queries = (
        await db.scalars(
            select(MedicalQuery)
            .where(MedicalQuery.patient_id == patient.id)
            .order_by(MedicalQuery.created_at.desc())
        )
    ).all()
    return [await _query_out(db, query) for query in queries]


@doctor_router.get("/queries", response_model=list[MedicalQueryOut])
async def doctor_queries(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user_dep),
) -> list[MedicalQueryOut]:
    _require_role(current_user, "doctor")
    doctor = await db.scalar(select(Doctor).where(Doctor.user_id == current_user.id))
    if doctor is None:
        raise NotFoundError("Doctor profile not found.")
    queries = (
        await db.scalars(
            select(MedicalQuery)
            .where(MedicalQuery.doctor_id == doctor.id)
            .order_by(MedicalQuery.created_at.desc())
        )
    ).all()
    return [await _query_out(db, query) for query in queries]


@doctor_router.put("/queries/{query_id}/answer", response_model=MedicalQueryOut)
async def answer_query(
    query_id: int,
    body: MedicalAnswer,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user_dep),
) -> MedicalQueryOut:
    _require_role(current_user, "doctor")
    doctor = await db.scalar(select(Doctor).where(Doctor.user_id == current_user.id))
    if doctor is None:
        raise NotFoundError("Doctor profile not found.")
    query = await db.scalar(
        select(MedicalQuery).where(
            MedicalQuery.id == query_id, MedicalQuery.doctor_id == doctor.id
        )
    )
    if query is None:
        raise NotFoundError("Query not found.")
    query.answer = body.answer.strip()
    query.status = "Answered"
    query.updated_at = datetime.now(timezone.utc)
    await db.commit()
    return await _query_out(db, query)


def _require_role(user: User, role: str) -> None:
    if user.role != role:
        raise ForbiddenError(f"{role.capitalize()} access required.")


async def _list_doctors(db: AsyncSession) -> list[DoctorSummary]:
    result = await db.execute(select(Doctor, User).join(User, Doctor.user_id == User.id))
    return [
        DoctorSummary(
            id=doctor.id,
            name=user.full_name,
            specialization=doctor.specialization,
            email=user.email,
            phone=doctor.phone or None,
        )
        for doctor, user in result.all()
    ]


async def _query_out(db: AsyncSession, query: MedicalQuery) -> MedicalQueryOut:
    patient = await db.get(PatientProfile, query.patient_id)
    doctor = await db.get(Doctor, query.doctor_id)
    if patient is None or doctor is None:
        raise NotFoundError("Query profile not found.")
    patient_user = await db.get(User, patient.user_id)
    doctor_user = await db.get(User, doctor.user_id)
    if patient_user is None or doctor_user is None:
        raise NotFoundError("Query account not found.")
    return MedicalQueryOut(
        id=query.id,
        patient_id=patient.id,
        patient_name=patient.name,
        doctor_id=doctor.id,
        doctor_name=doctor_user.full_name,
        title=query.title,
        description=query.description,
        answer=query.answer,
        status=query.status,
        created_at=query.created_at,
        updated_at=query.updated_at,
    )


router.include_router(auth_router)
router.include_router(admin_router)
router.include_router(patient_router)
router.include_router(doctor_router)
