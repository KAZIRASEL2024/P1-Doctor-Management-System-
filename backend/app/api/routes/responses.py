"""Doctor response submission routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import current_user_dep
from app.db.session import get_db
from app.models.user import User
from app.schemas.response import ResponseCreate, ResponseOut
from app.services import response_service

router = APIRouter(prefix="/responses", tags=["Responses"])


@router.post("", response_model=ResponseOut, status_code=201)
async def submit_response(
    body: ResponseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user_dep),
) -> ResponseOut:
    return await response_service.submit_response(db, body, current_user)
