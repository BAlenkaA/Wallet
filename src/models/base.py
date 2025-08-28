from sqlalchemy import Integer, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    metadata = MetaData()
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
