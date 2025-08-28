from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from crud.base import CRUDBase
from models import User


class CRUDUser(CRUDBase):
    async def get_profile_by_id(
        self,
        session: AsyncSession,
        user_id: int,
    ):
        statement = select(self.model).where(self.model.id == user_id)
        result = await session.execute(statement)
        return result.unique().scalars().one_or_none()

    async def get_profile_with_accounts(
        self,
        session: AsyncSession,
        user_id: int,
    ):
        statement = (
            select(self.model)
            .where(self.model.id == user_id)
            .options(
                joinedload(self.model.accounts),
            )
        )
        result = await session.execute(statement)
        return result.unique().scalars().one_or_none()


user_crud = CRUDUser(User)
