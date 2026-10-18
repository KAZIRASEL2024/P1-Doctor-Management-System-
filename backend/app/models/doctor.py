"""Doctor model — veterinarian profiles."""
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.doctor_zone_assignment import DoctorZoneAssignment
    from app.models.consultation_response import ConsultationResponse


class Doctor(Base):
    __tablename__ = "doctors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)

    # Professional details
    registration_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    specialization: Mapped[str] = mapped_column(String(255), nullable=False)
    qualification: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(30), nullable=False)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Emergency doctor flag — receives after-hours routed cases
    is_emergency_doctor: Mapped[bool] = mapped_column(default=False)
    is_available: Mapped[bool] = mapped_column(default=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="doctor_profile")
    zone_assignments: Mapped[List["DoctorZoneAssignment"]] = relationship(
        "DoctorZoneAssignment", back_populates="doctor"
    )
    responses: Mapped[List["ConsultationResponse"]] = relationship(
        "ConsultationResponse", back_populates="doctor"
    )

    def __repr__(self) -> str:
        return f"<Doctor id={self.id} reg={self.registration_number!r}>"
