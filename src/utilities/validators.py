import hashlib

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Administrator, Replenishment, User
from schemas.replenishment import WebhookRequest
from schemas.token import UserLogin
from security.password import check_password
from security.token import create_access_token


async def validate_user(
    user: UserLogin,
    db: AsyncSession,
) -> str:
    result = await db.execute(select(User).where(User.email == user.email))
    user_from_db = result.scalar_one_or_none()

    if user_from_db:
        if check_password(user.password, user_from_db.hashed_password):
            return create_access_token(
                data={"sub": user_from_db.email, "type": "user"})
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    result = await db.execute(
        select(Administrator).where(Administrator.email == user.email)
    )
    admin_from_db = result.scalar_one_or_none()
    if admin_from_db:
        if check_password(user.password, admin_from_db.hashed_password):
            return create_access_token(
                data={"sub": admin_from_db.email, "type": "admin"}
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
    )


async def existing_user(email: str, db: AsyncSession) -> bool:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none() is not None


async def validate_email_unique(email: str, db: AsyncSession) -> bool:
    result_user = await db.execute(select(User).where(User.email == email))
    if result_user.scalar_one_or_none():
        return False

    result_admin = await db.execute(
        select(Administrator).where(Administrator.email == email)
    )
    if result_admin.scalar_one_or_none():
        return False

    return True


def verify_signature(data: WebhookRequest, secret_key: str) -> bool:
    signature_string = (
        f"{data.account_id}{data.amount}{data.transaction_id}{data.user_id}"
        f"{secret_key}"
    )
    computed_signature = hashlib.sha256(signature_string.encode()).hexdigest()
    return computed_signature == data.signature


async def existing_transaction(transaction_id: str, db: AsyncSession) -> bool:
    result = await db.execute(
        select(Replenishment)
        .where(Replenishment.transaction_id == transaction_id)
    )
    return result.scalar_one_or_none() is not None
