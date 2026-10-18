"""Consultation CRUD service."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.consultation import Consultation
from app.models.zone import Zone
from app.schemas.consultation import (
    ConsultationDetail,
    ConsultationListItem,
    ConsultationListResponse,
)
from app.core.exceptions import NotFoundError


def _list_item_from_orm(c: Consultation) -> ConsultationListItem:
    return ConsultationListItem(
        id=c.id,
        aisp_reference=c.aisp_reference,
        zone_id=c.zone_id,
        zone_name=c.zone.name if c.zone else None,
        field_worker_name=c.field_worker_name,
        animal_species=c.animal_species,
        animal_breed=c.animal_breed,
        symptoms=c.symptoms,
        priority=c.priority,
        status=c.status,
        submitted_at=c.submitted_at,
        sla_deadline=c.sla_deadline,
        responded_at=c.responded_at,
    )


def _detail_from_orm(c: Consultation) -> ConsultationDetail:
    return ConsultationDetail(
        id=c.id,
        aisp_reference=c.aisp_reference,
        zone_id=c.zone_id,
        zone_name=c.zone.name if c.zone else None,
        field_worker_name=c.field_worker_name,
        field_worker_phone=c.field_worker_phone,
        animal_species=c.animal_species,
        animal_breed=c.animal_breed,
        animal_age_months=c.animal_age_months,
        animal_weight_kg=c.animal_weight_kg,
        animal_temperature_celsius=c.animal_temperature_celsius,
        animal_owner_name=c.animal_owner_name,
        symptoms=c.symptoms,
        remarks=c.remarks,
        priority=c.priority,
        status=c.status,
        submitted_at=c.submitted_at,
        sla_deadline=c.sla_deadline,
        responded_at=c.responded_at,
        closed_at=c.closed_at,
        attachments=c.attachments,
        responses=c.responses,
    )


async def list_consultations(
    db: AsyncSession,
    page: int = 1,
    page_size: int = 20,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    zone_id: Optional[int] = None,
    search: Optional[str] = None,
) -> ConsultationListResponse:
    query = (
        select(Consultation)
        .options(selectinload(Consultation.zone))
        .order_by(Consultation.submitted_at.desc())
    )
    if status:
        query = query.where(Consultation.status == status)
    if priority:
        query = query.where(Consultation.priority == priority)
    if zone_id:
        query = query.where(Consultation.zone_id == zone_id)
    if search:
        like = f"%{search}%"
        query = query.where(
            Consultation.field_worker_name.ilike(like)
            | Consultation.animal_species.ilike(like)
            | Consultation.symptoms.ilike(like)
        )

    # Count total
    count_q = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_q)).scalar_one()

    # Paginate
    offset = (page - 1) * page_size
    result = await db.execute(query.offset(offset).limit(page_size))
    rows = result.scalars().all()

    return ConsultationListResponse(
        items=[_list_item_from_orm(c) for c in rows],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=math.ceil(total / page_size) if total > 0 else 1,
    )


async def get_consultation(db: AsyncSession, consultation_id: int) -> ConsultationDetail:
    result = await db.execute(
        select(Consultation)
        .where(Consultation.id == consultation_id)
        .options(
            selectinload(Consultation.zone),
            selectinload(Consultation.attachments),
            selectinload(Consultation.responses),
        )
    )
    c = result.scalar_one_or_none()
    if c is None:
        raise NotFoundError(f"Consultation {consultation_id} not found.")
    return _detail_from_orm(c)
