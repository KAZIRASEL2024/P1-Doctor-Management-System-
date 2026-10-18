"""Additional consultation tests."""
import pytest
from app.core.security import hash_password
from app.models.user import User
from app.models.zone import Zone
from app.models.consultation import Consultation
from datetime import datetime, timezone


async def create_admin_and_token(client, db_session):
    user = User(
        email="admin@test.com",
        hashed_password=hash_password("Admin@1234"),
        full_name="Test Admin",
        role="admin",
    )
    db_session.add(user)
    await db_session.commit()
    login = await client.post("/api/auth/login", json={"email": "admin@test.com", "password": "Admin@1234"})
    return login.json()["access_token"]


@pytest.mark.asyncio
async def test_list_consultations_empty(client, db_session):
    token = await create_admin_and_token(client, db_session)
    r = await client.get("/api/consultations", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 0
    assert data["items"] == []


@pytest.mark.asyncio
async def test_list_consultations_with_data(client, db_session):
    token = await create_admin_and_token(client, db_session)

    zone = Zone(name="Test Zone", is_active=True)
    db_session.add(zone)
    await db_session.flush()

    c = Consultation(
        field_worker_name="Test Worker",
        animal_species="Cattle",
        symptoms="Cough and lethargy",
        priority="normal",
        status="pending",
        zone_id=zone.id,
        submitted_at=datetime.now(timezone.utc),
    )
    db_session.add(c)
    await db_session.commit()

    r = await client.get("/api/consultations", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["total"] == 1


@pytest.mark.asyncio
async def test_get_consultation_not_found(client, db_session):
    token = await create_admin_and_token(client, db_session)
    r = await client.get("/api/consultations/99999", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_list_requires_auth(client):
    r = await client.get("/api/consultations")
    assert r.status_code == 401
