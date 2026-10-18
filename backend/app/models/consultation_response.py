"""ConsultationResponse model — doctor feedback on a consultation."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.consultation import Consultation
    from app.models.doctor import Doctor


class ConsultationResponse(Base):
    __tablename__ = "consultation_responses"

    id: Mapped[int] = mapped_column(primary_key=True)
    consultation_id: Mapped[int] = mapped_column(
        ForeignKey("consultations.id"), nullable=False, index=True
    )
    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctors.id"), nullable=False, index=True
    )

    diagnosis: Mapped[str] = mapped_column(Text, nullable=False)
    treatment_plan: Mapped[str] = mapped_column(Text, nullable=False)
    medications: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    follow_up_instructions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_emergency_referral: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    consultation: Mapped["Consultation"] = relationship(
        "Consultation", back_populates="responses"
    )
    doctor: Mapped["Doctor"] = relationship("Doctor", back_populates="responses")
