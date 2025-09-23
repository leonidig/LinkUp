from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .. import Base


class User(Base):
    __tablename__ = "users"

    tg_id: Mapped[int]
    username: Mapped[str] = mapped_column(nullable=True)
    phone: Mapped[int]
    name: Mapped[str]
    role: Mapped[str] = mapped_column(default="user")  # user, master, admin

    master: Mapped["Master"] = relationship(back_populates="user", uselist=False)
    orders: Mapped[list["Order"]] = relationship(back_populates="user")
    referrals: Mapped[int] = mapped_column(default=0)