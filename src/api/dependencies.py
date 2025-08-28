from typing import Type, TypeVar

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from databases.database import get_async_session
from models import Administrator, User
from security.token import decode_access_token

T = TypeVar("T", User, Administrator)
bearer_scheme = HTTPBearer()


async def get_email_from_token(token: str) -> str:
    try:
        payload = decode_access_token(token)
        email = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        return email
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


async def get_user_by_email(email: str, db: AsyncSession, model: Type[T]) -> T:
    result = await db.execute(select(model).where(model.email == email))
    user_data = result.scalar_one_or_none()

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user_data


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_async_session),
) -> User:
    """
    Retrieves the current user from the db.
    """
    token = credentials.credentials
    email = await get_email_from_token(token)
    return await get_user_by_email(email, db, User)


async def get_admin_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_async_session),
) -> Administrator:
    """
    Retrieves the admin user from the db.
    """
    token = credentials.credentials
    email = await get_email_from_token(token)
    return await get_user_by_email(email, db, Administrator)
