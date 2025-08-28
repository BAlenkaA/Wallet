from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Administrator(Base):
    """
    Модель администратора.
    Представляет собой учётную запись администратора с информацией об имени,
     фамилии, адресе электронной почты и пароле.

    Args:
        email (str): Адрес электронной почты администратора
        hashed_password (str): Зашифрованный пароль администратора
        first_name (str): Имя администратора
        last_name (str): Фамилия администратора
        created_at (datetime): Дата создания аккаунта
        updated_at (datetime): Дата последнего изменения аккаунта
    """

    __tablename__ = "administrators"
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

    @property
    def full_name(self) -> str:
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name
