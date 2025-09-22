from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .. import Base
from .user import User


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    master_id: Mapped[int] = mapped_column(ForeignKey("masters.id"))
    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow) # TODO fix deprecated
    status: Mapped[str] = mapped_column(default="active")  # active / closed

    master: Mapped['Master'] = relationship(back_populates="services")
    orders: Mapped[list["Order"]] = relationship(back_populates="service")