from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .. import Base
from .user import User


class OrderStatus(str, Enum):
    pending = "очікується"
    confirmed = "прийнято"
    completed = "виконано"
    cancelled = "відхилено"


class Order(Base):
    __tablename__ = "orders"


    status: Mapped[OrderStatus] = mapped_column(default=OrderStatus.pending)
    scheduled_at: Mapped[datetime]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    price: Mapped[int]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    master_id: Mapped[int] = mapped_column(ForeignKey("masters.id"))
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), nullable=True)

    user: Mapped[User] = relationship(back_populates="orders")
    master: Mapped['Master'] = relationship(back_populates="orders")
    service: Mapped['Service'] = relationship(back_populates="orders")