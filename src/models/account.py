from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models import User


class Account(Base):
    """
    Модель счета пользователя.

    Представляет собой банковский или виртуальный счет, принадлежащий
     пользователю.
    Содержит информацию о балансе и истории операций.

    Args:
        user_id (int): Идентификатор пользователя, которому принадлежит счет
        balance (int): Баланс счета
        created_at (datetime): Дата создания счета
        updated_at (datetime): Дата последнего изменения счета
    """

    __tablename__ = "accounts"
    user_id: Mapped[str] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    balance: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    user: Mapped["User"] = relationship("User", back_populates="accounts")
