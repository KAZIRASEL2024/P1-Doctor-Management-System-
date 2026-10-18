"""Auth endpoint tests."""
import pytest

from app.core.security import hash_password
from app.models.user import User


async def create_test_user(db_session, role="doctor"):
    user = User(
        email="test@example.com",
        hashed_password=hash_password("Test@1234"),
        full_name="Test User",
        role=role,
    )
    db_session.add(user)
    await db_session.commit()
    return user


@pytest.mark.asyncio
async def test_login_success(client, db_session):
    await create_test_user(db_session)
    response = await client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "Test@1234"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["role"] == "doctor"


@pytest.mark.asyncio
async def test_oauth2_password_token(client, db_session):
    await create_test_user(db_session)
    response = await client.post(
        "/api/v1/auth/token",
        data={"username": "test@example.com", "password": "Test@1234"},
    )
    assert response.status_code == 200
    assert response.json()["role"] == "doctor"


@pytest.mark.asyncio
async def test_login_wrong_password(client, db_session):
    await create_test_user(db_session)
    response = await client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "WrongPassword"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_requires_auth(client):
    response = await client.get("/api/auth/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_returns_user(client, db_session):
    await create_test_user(db_session)
    login = await client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "Test@1234"},
    )
    token = login.json()["access_token"]
    response = await client.get(
        "/api/auth/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
