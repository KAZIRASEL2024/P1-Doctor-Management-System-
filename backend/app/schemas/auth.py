"""Auth schemas."""
from __future__ import annotations

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
    role: str


class CurrentUserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool

    model_config = {"from_attributes": True}
