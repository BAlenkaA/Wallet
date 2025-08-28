from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models import User


class Replenishment(Base):
    """
    Модель пополнения счета.

    Представляет собой запись о пополнении баланса пользователя.
    Содержит информацию о транзакции, сумме пополнения и пользователе.

    Args:
        transaction_id (str): Уникальный идентификатор транзакции в
         "сторонней системе"
        user_id (int): Уникальный идентификатор счета пользователя
        amount (int): Сумма пополнения счета
        created_at (datetime): Дата создания пополнения
    """

    __tablename__ = "replenishments"
    transaction_id: Mapped[str] = mapped_column(
        String, unique=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    amount: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped["User"] = relationship(
        "User", back_populates="replenishments")
