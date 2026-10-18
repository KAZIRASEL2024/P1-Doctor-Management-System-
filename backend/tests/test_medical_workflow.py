"""Human patient/doctor workflow tests."""
import pytest

from app.core.security import hash_password
from app.models.user import User


@pytest.mark.asyncio
async def test_patient_query_and_doctor_answer_flow(client, db_session):
    patient_registration = await client.post(
        "/api/v1/patient/register",
        json={
            "email": "patient@example.com",
            "password": "PatientPass123",
            "name": "Sam Patient",
            "age": 34,
            "gender": "Female",
            "contact_details": "+1 555 0100",
        },
    )
    assert patient_registration.status_code == 201

    db_session.add(
        User(
            email="admin@workflow.example.com",
            hashed_password=hash_password("AdminPass123"),
            full_name="Workflow Admin",
            role="admin",
        )
    )
    await db_session.commit()

    admin_login = await client.post(
        "/api/auth/login",
        json={"email": "admin@workflow.example.com", "password": "AdminPass123"},
    )
    assert admin_login.status_code == 200, admin_login.text
    admin_headers = {"Authorization": f"Bearer {admin_login.json()['access_token']}"}
    doctor_creation = await client.post(
        "/api/v1/admin/doctors",
        headers=admin_headers,
        json={
            "name": "Dr. Lee",
            "specialization": "Cardiology",
            "email": "doctor@workflow.example.com",
            "password": "DoctorPass123",
            "phone": "555-0101",
        },
    )
    assert doctor_creation.status_code == 201
    doctor_id = doctor_creation.json()["id"]

    patient_login = await client.post(
        "/api/v1/auth/login",
        json={"email": "patient@example.com", "password": "PatientPass123"},
    )
    assert patient_login.json()["role"] == "patient"
    patient_headers = {"Authorization": f"Bearer {patient_login.json()['access_token']}"}
    submitted = await client.post(
        "/api/v1/patient/queries",
        headers=patient_headers,
        json={
            "doctor_id": doctor_id,
            "title": "Recurring headache",
            "description": "I have had a headache for three days.",
        },
    )
    assert submitted.status_code == 201
    query_id = submitted.json()["id"]
    assert submitted.json()["status"] == "Pending"

    doctor_login = await client.post(
        "/api/v1/auth/login",
        json={"email": "doctor@workflow.example.com", "password": "DoctorPass123"},
    )
    doctor_headers = {"Authorization": f"Bearer {doctor_login.json()['access_token']}"}
    doctor_queries = await client.get("/api/v1/doctor/queries", headers=doctor_headers)
    assert [query["id"] for query in doctor_queries.json()] == [query_id]

    response = await client.put(
        f"/api/v1/doctor/queries/{query_id}/answer",
        headers=doctor_headers,
        json={"answer": "Please arrange an in-person evaluation."},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "Answered"

    patient_queries = await client.get("/api/v1/patient/queries", headers=patient_headers)
    assert patient_queries.json()[0]["answer"] == "Please arrange an in-person evaluation."


@pytest.mark.asyncio
async def test_patient_cannot_create_doctor_accounts(client):
    registration = await client.post(
        "/api/v1/patient/register",
        json={
            "email": "patient2@example.com",
            "password": "PatientPass123",
            "name": "Another Patient",
            "age": 20,
            "gender": "Male",
            "contact_details": "555-0200",
        },
    )
    assert registration.status_code == 201
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "patient2@example.com", "password": "PatientPass123"},
    )
    response = await client.post(
        "/api/v1/admin/doctors",
        headers={"Authorization": f"Bearer {login.json()['access_token']}"},
        json={
            "name": "Unauthorized Doctor",
            "specialization": "General Medicine",
            "email": "unauthorized-doctor@example.com",
            "password": "DoctorPass123",
        },
    )
    assert response.status_code == 403
