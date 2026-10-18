"""Doctor response service."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import ForbiddenError, NotFoundError
from app.models.consultation import Consultation
from app.models.consultation_response import ConsultationResponse
from app.models.doctor import Doctor
from app.models.notification import Notification
from app.models.user import User
from app.schemas.response import ResponseCreate, ResponseOut


async def submit_response(
    db: AsyncSession,
    data: ResponseCreate,
    current_user: User,
) -> ResponseOut:
    # Resolve doctor profile
    result = await db.execute(
        select(Doctor).where(Doctor.user_id == current_user.id)
    )
    doctor = result.scalar_one_or_none()
    if doctor is None and current_user.role != "admin":
        raise ForbiddenError("No doctor profile found for this user.")

    # Validate consultation exists
    c_result = await db.execute(
        select(Consultation)
        .where(Consultation.id == data.consultation_id)
        .options(selectinload(Consultation.zone))
    )
    consultation = c_result.scalar_one_or_none()
    if consultation is None:
        raise NotFoundError(f"Consultation {data.consultation_id} not found.")

    # Zone access check (doctors only)
    if current_user.role == "doctor" and doctor:
        assigned = await db.execute(
            select(Doctor)
            .where(Doctor.id == doctor.id)
            .options(selectinload(Doctor.zone_assignments))
        )
        d = assigned.scalar_one()
        zone_ids = {a.zone_id for a in d.zone_assignments}
        if consultation.zone_id and consultation.zone_id not in zone_ids:
            raise ForbiddenError("You are not assigned to this consultation's zone.")

    # Create response
    response = ConsultationResponse(
        consultation_id=data.consultation_id,
        doctor_id=doctor.id if doctor else 0,
        diagnosis=data.diagnosis,
        treatment_plan=data.treatment_plan,
        medications=data.medications,
        follow_up_instructions=data.follow_up_instructions,
        is_emergency_referral=data.is_emergency_referral,
    )
    db.add(response)

    # Update consultation status
    consultation.status = "responded"
    consultation.responded_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(response)
    return ResponseOut.model_validate(response)
