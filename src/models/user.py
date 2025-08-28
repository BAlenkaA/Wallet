from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models import Account, Replenishment


class User(Base):
    """
    Модель пользователя.

    Представляет собой учетную запись пользователя с информацией об имени,
     фамилии, адресе электронной почты и пароле.

    Args:
        email (str): Адрес электронной почты пользователя
        hashed_password (str): Хеш пароля пользователя
        first_name (str): Имя пользователя
        last_name (str, optional): Фамилия пользователя
        created_at (datetime): Дата создания учетной записи
        updated_at (datetime): Дата последнего изменения учетной записи
    """

    __tablename__ = "users"
    email: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    accounts: Mapped[List["Account"]] = relationship(
        "Account", back_populates="user")
    replenishments: Mapped[List["Replenishment"]] = relationship(
        "Replenishment", back_populates="user"
    )

    @property
    def full_name(self) -> str:
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name
