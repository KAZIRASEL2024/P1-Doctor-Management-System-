"""Authentication service."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import UnauthorizedError
from app.core.security import create_access_token, decode_access_token, verify_password
from app.core.config import settings
from app.models.user import User


async def authenticate_user(
    db: AsyncSession, email: str, password: str
) -> User:
    result = await db.execute(select(User).where(User.email == email.lower()))
    user = result.scalar_one_or_none()
    if user is None or not verify_password(password, user.hashed_password):
        raise UnauthorizedError("Invalid email or password.")
    if not user.is_active:
        raise UnauthorizedError("Account is disabled.")
    # Update last login timestamp
    user.last_login_at = datetime.now(timezone.utc)
    await db.commit()
    return user


def issue_token(user: User) -> dict:
    token = create_access_token(
        subject=user.id,
        extra_claims={"role": user.role, "name": user.full_name},
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "role": user.role,
    }


async def get_current_user(db: AsyncSession, token: str) -> User:
    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise UnauthorizedError("Invalid or expired token.")

    result = await db.execute(
        select(User)
        .where(User.id == user_id)
        .options(selectinload(User.doctor_profile))
    )
    user = result.scalar_one_or_none()
    if user is None or not user.is_active:
        raise UnauthorizedError("User not found or inactive.")
    return user
