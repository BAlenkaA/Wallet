from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_current_user
from crud.replenishment import replenishment_crud
from crud.user import user_crud
from databases.database import get_async_session
from models import User
from schemas.replenishment import PaymentResponse
from schemas.user import UserProfile, UserProfileWithAccounts

router = APIRouter()


@router.get("/me", response_model=UserProfile)
async def user_profile(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    return await user_crud.get_profile_by_id(
        db,
        user.id,
    )


@router.get("/accounts", response_model=UserProfileWithAccounts)
async def get_user_accounts(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    return await user_crud.get_profile_with_accounts(db, user.id)


@router.get("/payments", response_model=list[PaymentResponse])
async def get_user_payments(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    return await replenishment_crud.get_user_payments(db, user.id)
