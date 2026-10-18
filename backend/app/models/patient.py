"""Animal patient model."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    species: Mapped[str] = mapped_column(String(100), nullable=False)
    breed: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    sex: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    age_months: Mapped[Optional[int]] = mapped_column(nullable=True)
    weight_kg: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    owner_name: Mapped[str] = mapped_column(String(255), nullable=False)
    owner_phone: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    medical_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<Patient id={self.id} name={self.name!r}>"
