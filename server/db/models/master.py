from sqlalchemy import ForeignKey 
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .. import Base
from .user import User


class Master(Base):
    __tablename__ = "masters"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    specialization: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    experience_years: Mapped[int] = mapped_column(default=0)
    location: Mapped[str] = mapped_column(nullable=True)
    schedule: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    rating: Mapped[float] = mapped_column(default=0.0)
    reviews_count: Mapped[int] = mapped_column(default=0)
    referral_bonus: Mapped[int] = mapped_column(default=0)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    user: Mapped[User] = relationship(back_populates="master")

    orders: Mapped[list["Order"]] = relationship(back_populates="master")
    services: Mapped[list["Service"]] = relationship(back_populates="master")
    referral_links: Mapped[list["ReferralLink"]] = relationship(back_populates="master")
