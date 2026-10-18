"""Doctor ↔ Zone many-to-many assignment."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.doctor import Doctor
    from app.models.zone import Zone


class DoctorZoneAssignment(Base):
    __tablename__ = "doctor_zone_assignments"

    id: Mapped[int] = mapped_column(primary_key=True)
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"), nullable=False, index=True)
    zone_id: Mapped[int] = mapped_column(ForeignKey("zones.id"), nullable=False, index=True)
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    assigned_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Relationships
    doctor: Mapped["Doctor"] = relationship("Doctor", back_populates="zone_assignments")
    zone: Mapped["Zone"] = relationship("Zone", back_populates="doctor_assignments")
