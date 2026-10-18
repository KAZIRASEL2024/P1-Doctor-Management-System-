"""Zone model — geographic regions aligned with BRAC ERP region codes."""
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.doctor_zone_assignment import DoctorZoneAssignment
    from app.models.consultation import Consultation


class Zone(Base):
    __tablename__ = "zones"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    # erp_region_code maps to the existing BRAC ERP system.
    # Set to NULL until ERP integration is confirmed.
    erp_region_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    # Relationships
    doctor_assignments: Mapped[List["DoctorZoneAssignment"]] = relationship(
        "DoctorZoneAssignment", back_populates="zone"
    )
    consultations: Mapped[List["Consultation"]] = relationship(
        "Consultation", back_populates="zone"
    )

    def __repr__(self) -> str:
        return f"<Zone id={self.id} name={self.name!r}>"
