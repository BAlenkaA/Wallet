from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from databases.database import get_async_session
from schemas.token import Token, UserLogin
from utilities.validators import validate_user

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_user(
        user: UserLogin, db: AsyncSession = Depends(get_async_session)):
    access_token = await validate_user(user, db)
    return {"access_token": access_token, "token_type": "bearer"}
