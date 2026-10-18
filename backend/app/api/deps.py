"""FastAPI dependency: extract and validate the current user from Bearer token."""
from __future__ import annotations

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.services.auth_service import get_current_user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


async def current_user_dep(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    return await get_current_user(db, token)
