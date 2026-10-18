"""Role-based permission helpers.

Roles
-----
admin       — Full system access.
doctor      — Can view/respond to consultations in their assigned zones only.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from app.core.exceptions import ForbiddenError

if TYPE_CHECKING:
    from app.models.user import User


def require_admin(current_user: "User") -> None:
    if current_user.role != "admin":
        raise ForbiddenError("Admin access required.")


def require_doctor_or_admin(current_user: "User") -> None:
    if current_user.role not in ("doctor", "admin"):
        raise ForbiddenError("Doctor or admin access required.")


def check_zone_access(current_user: "User", zone_id: int) -> None:
    """Raise ForbiddenError if a non-admin doctor is not assigned to zone_id."""
    if current_user.role == "admin":
        return
    doctor = current_user.doctor_profile
    if doctor is None:
        raise ForbiddenError("No doctor profile linked to this account.")
    assigned_zone_ids = {a.zone_id for a in doctor.zone_assignments}
    if zone_id not in assigned_zone_ids:
        raise ForbiddenError("You are not assigned to this zone.")
