"""Consultation model — animal health consultation submitted by AISP field workers."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.zone import Zone
    from app.models.attachment import Attachment
    from app.models.consultation_response import ConsultationResponse


class Consultation(Base):
    __tablename__ = "consultations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Reference to the originating AISP system (external ID — not modified here)
    aisp_reference: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, index=True, comment="External AISP case reference"
    )

    # Zone/region where the case originated
    zone_id: Mapped[Optional[int]] = mapped_column(ForeignKey("zones.id"), nullable=True)

    # Field worker info (from AISP — stored for display purposes)
    field_worker_name: Mapped[str] = mapped_column(String(255), nullable=False)
    field_worker_phone: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)

    # Animal details
    animal_species: Mapped[str] = mapped_column(String(100), nullable=False)
    animal_breed: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    animal_age_months: Mapped[Optional[int]] = mapped_column(nullable=True)
    animal_weight_kg: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    animal_temperature_celsius: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    animal_owner_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Clinical information
    symptoms: Mapped[str] = mapped_column(Text, nullable=False)
    remarks: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    priority: Mapped[str] = mapped_column(
        String(20), nullable=False, default="normal"
        # priority ∈ {"normal", "urgent", "emergency"}
    )

    # Workflow status
    status: Mapped[str] = mapped_column(
        String(30), nullable=False, default="pending"
        # status ∈ {"pending", "in_progress", "responded", "closed", "overdue"}
    )

    # Timestamps
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    responded_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    sla_deadline: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    zone: Mapped[Optional["Zone"]] = relationship("Zone", back_populates="consultations")
    attachments: Mapped[List["Attachment"]] = relationship(
        "Attachment", back_populates="consultation", cascade="all, delete-orphan"
    )
    responses: Mapped[List["ConsultationResponse"]] = relationship(
        "ConsultationResponse", back_populates="consultation", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Consultation id={self.id} status={self.status!r}>"
