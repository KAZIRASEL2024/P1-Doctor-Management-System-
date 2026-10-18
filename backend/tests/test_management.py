"""Doctor creation and animal patient profile API tests."""
import pytest

from app.core.security import hash_password
from app.models.user import User


async def create_admin(db_session):
    admin = User(
        email="admin.management@test.com",
        hashed_password=hash_password("Admin@1234"),
        full_name="Management Admin",
        role="admin",
    )
    db_session.add(admin)
    await db_session.commit()
    return admin


async def admin_headers(client, db_session):
    await create_admin(db_session)
    response = await client.post(
        "/api/auth/login",
        json={"email": "admin.management@test.com", "password": "Admin@1234"},
    )
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest.mark.asyncio
async def test_create_and_view_patient_profile(client, db_session):
    headers = await admin_headers(client, db_session)
    response = await client.post(
        "/api/patients",
        headers=headers,
        json={
            "name": "Moyna",
            "species": "Goat",
            "breed": "Black Bengal",
            "sex": "female",
            "age_months": 18,
            "weight_kg": 24.5,
            "owner_name": "Amina Begum",
            "owner_phone": "+8801700000000",
            "location": "Dhaka Central",
            "medical_notes": "Previous vaccination recorded.",
        },
    )

    assert response.status_code == 201
    patient = response.json()
    assert patient["name"] == "Moyna"
    assert patient["owner_name"] == "Amina Begum"

    detail = await client.get(f"/api/patients/{patient['id']}", headers=headers)
    listing = await client.get("/api/patients", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["medical_notes"] == "Previous vaccination recorded."
    assert listing.json()["total"] == 1


@pytest.mark.asyncio
async def test_create_doctor_account_and_profile(client, db_session):
    headers = await admin_headers(client, db_session)
    response = await client.post(
        "/api/doctors",
        headers=headers,
        json={
            "full_name": "Dr. Test Veterinarian",
            "email": "doctor.management@test.com",
            "password": "Doctor@1234",
            "registration_number": "VET-MANAGEMENT-001",
            "specialization": "Large Animal Medicine",
            "qualification": "BVSc & AH",
            "phone": "+8801700000001",
            "is_emergency_doctor": False,
            "is_available": True,
            "zone_ids": [],
        },
    )

    assert response.status_code == 201
    doctor = response.json()
    assert doctor["full_name"] == "Dr. Test Veterinarian"
    assert doctor["email"] == "doctor.management@test.com"

    login = await client.post(
        "/api/auth/login",
        json={"email": "doctor.management@test.com", "password": "Doctor@1234"},
    )
    assert login.status_code == 200

    detail = await client.get(f"/api/doctors/{doctor['id']}", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["registration_number"] == "VET-MANAGEMENT-001"


@pytest.mark.asyncio
async def test_doctor_creation_requires_admin(client, db_session):
    user = User(
        email="doctor.nonadmin@test.com",
        hashed_password=hash_password("Doctor@1234"),
        full_name="Regular Doctor",
        role="doctor",
    )
    db_session.add(user)
    await db_session.commit()
    login = await client.post(
        "/api/auth/login",
        json={"email": user.email, "password": "Doctor@1234"},
    )
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    response = await client.post(
        "/api/doctors",
        headers=headers,
        json={
            "full_name": "Dr. Not Allowed",
            "email": "doctor.denied@test.com",
            "password": "Doctor@1234",
            "registration_number": "VET-DENIED-001",
            "specialization": "General",
            "qualification": "BVSc",
            "phone": "+8801700000002",
        },
    )
    assert response.status_code == 403
