from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models import Replenishment


class CRUDReplenishment(CRUDBase):

    async def get_user_payments(
        self,
        session: AsyncSession,
        user_id: int,
    ):
        statement = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .order_by(self.model.created_at.desc())
        )
        result = await session.execute(statement)
        return result.unique().scalars().all()


replenishment_crud = CRUDReplenishment(Replenishment)
