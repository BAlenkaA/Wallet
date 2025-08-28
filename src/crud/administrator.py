from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models import Administrator


class CRUDAdministrator(CRUDBase):
    async def get_admin_profile_by_id(
        self,
        session: AsyncSession,
        admin_id: int,
    ):
        statement = select(self.model).where(self.model.id == admin_id)
        result = await session.execute(statement)
        return result.unique().scalars().one()


admin_crud = CRUDAdministrator(Administrator)
