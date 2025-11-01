from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .. import Base
from .user import User


class OrderStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"
    # rated = "rated"


class Order(Base):
    __tablename__ = "orders"


    status: Mapped[OrderStatus] = mapped_column(default=OrderStatus.pending)
    scheduled_at: Mapped[datetime] = mapped_column(nullable=True)
    deadline: Mapped[datetime] = mapped_column(nullable=True)
    description: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    price: Mapped[int]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    master_id: Mapped[int] = mapped_column(ForeignKey("masters.id"))
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), nullable=True)

    user: Mapped[User] = relationship(back_populates="orders")
    master: Mapped['Master'] = relationship(back_populates="orders")
    service: Mapped['Service'] = relationship(back_populates="orders")