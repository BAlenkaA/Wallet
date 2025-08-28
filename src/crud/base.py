from sqlalchemy import desc, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_multi(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 50
    ):
        db_objs = await session.execute(
            select(self.model)
            .order_by(desc(self.model.id))
            .offset(skip)
            .limit(limit)
        )
        return db_objs.scalars().all()

    async def create(
        self,
        create_schema,
        session: AsyncSession,
        commit: bool = True,
    ):
        data = create_schema.model_dump(exclude_unset=True)
        stmt = insert(self.model).values(**data).returning(self.model)
        result = await session.execute(stmt)
        obj = result.scalars().first()
        if commit:
            await session.commit()
            await session.refresh(obj)
        return obj

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
        commit: bool = True,
    ):
        update_data = obj_in.model_dump(exclude_unset=True)

        stmt = (
            update(self.model)
            .where(self.model.id == db_obj.id)
            .values(**update_data)
            .returning(self.model)
        )
        result = await session.execute(stmt)
        obj = result.scalars().first()
        if commit:
            await session.commit()
            await session.refresh(obj)
        return obj

    async def remove(
        self,
        db_obj,
        session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj
