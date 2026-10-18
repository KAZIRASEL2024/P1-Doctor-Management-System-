"""Doctor zone access restriction tests."""
import pytest
from app.core.security import hash_password
from app.models.user import User
from app.models.doctor import Doctor
from app.models.zone import Zone
from app.models.consultation import Consultation
from app.models.doctor_zone_assignment import DoctorZoneAssignment
from app.models.consultation_response import ConsultationResponse
from datetime import datetime, timezone


async def setup_doctor_with_zone(db_session, zone_ids: list):
    """Creates a doctor user assigned to specified zone_ids."""
    user = User(
        email="doctor.access@test.com",
        hashed_password=hash_password("Doctor@1234"),
        full_name="Dr. Zone Test",
        role="doctor",
    )
    db_session.add(user)
    await db_session.flush()

    doc = Doctor(
        user_id=user.id,
        registration_number="VET-TEST-001",
        specialization="General",
        qualification="BVSc",
        phone="+880-111-000",
    )
    db_session.add(doc)
    await db_session.flush()

    for zid in zone_ids:
        db_session.add(DoctorZoneAssignment(doctor_id=doc.id, zone_id=zid))
    await db_session.commit()
    return user, doc


@pytest.mark.asyncio
async def test_doctor_can_respond_to_own_zone(client, db_session):
    zone = Zone(name="Zone A", is_active=True)
    db_session.add(zone)
    await db_session.flush()

    user, doc = await setup_doctor_with_zone(db_session, [zone.id])

    consult = Consultation(
        field_worker_name="Worker",
        animal_species="Goat",
        symptoms="Fever",
        priority="normal",
        status="pending",
        zone_id=zone.id,
        submitted_at=datetime.now(timezone.utc),
    )
    db_session.add(consult)
    await db_session.commit()

    login = await client.post("/api/auth/login", json={"email": "doctor.access@test.com", "password": "Doctor@1234"})
    token = login.json()["access_token"]

    r = await client.post("/api/responses", headers={"Authorization": f"Bearer {token}"}, json={
        "consultation_id": consult.id,
        "diagnosis": "Mild fever, likely viral",
        "treatment_plan": "Rest and hydration for 3 days",
    })
    assert r.status_code == 201


@pytest.mark.asyncio
async def test_doctor_blocked_from_other_zone(client, db_session):
    zone_a = Zone(name="Zone A2", is_active=True)
    zone_b = Zone(name="Zone B2", is_active=True)
    db_session.add_all([zone_a, zone_b])
    await db_session.flush()

    # Doctor only assigned to zone_a
    user, doc = await setup_doctor_with_zone(db_session, [zone_a.id])

    # Consultation belongs to zone_b
    consult = Consultation(
        field_worker_name="Worker",
        animal_species="Cow",
        symptoms="Limping",
        priority="normal",
        status="pending",
        zone_id=zone_b.id,
        submitted_at=datetime.now(timezone.utc),
    )
    db_session.add(consult)
    await db_session.commit()

    login = await client.post("/api/auth/login", json={"email": "doctor.access@test.com", "password": "Doctor@1234"})
    token = login.json()["access_token"]

    r = await client.post("/api/responses", headers={"Authorization": f"Bearer {token}"}, json={
        "consultation_id": consult.id,
        "diagnosis": "Suspected foot rot infection",
        "treatment_plan": "Apply zinc sulphate foot bath twice daily for 5 days",
    })
    assert r.status_code == 403
