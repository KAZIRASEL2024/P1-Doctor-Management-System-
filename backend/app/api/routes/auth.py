"""Auth routes: login and current user."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import current_user_dep
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import CurrentUserResponse, LoginRequest, TokenResponse
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    user = await auth_service.authenticate_user(db, body.email, body.password)
    token_data = auth_service.issue_token(user)
    return TokenResponse(**token_data)


@router.get("/me", response_model=CurrentUserResponse)
async def me(current_user: User = Depends(current_user_dep)) -> CurrentUserResponse:
    return CurrentUserResponse.model_validate(current_user)
