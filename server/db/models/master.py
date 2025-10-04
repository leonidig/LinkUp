from sqlalchemy import ForeignKey 
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .. import Base


class Master(Base):
    __tablename__ = "masters"

    specialization: Mapped[str]
    description: Mapped[str]
    experience_years: Mapped[int] = mapped_column(default=0)
    location: Mapped[str]
    schedule: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    rating: Mapped[float] = mapped_column(default=0.0)
    # reviews_count: Mapped[int] = mapped_column(default=0)
    bad_grades: Mapped[int] = mapped_column(default=0)
    good_grades: Mapped[int] = mapped_column(default=0)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"), unique=True)
    user: Mapped['User'] = relationship(back_populates="master")

    orders: Mapped[list["Order"]] = relationship(back_populates="master")
    services: Mapped[list["Service"]] = relationship(back_populates="master")
    referral_links: Mapped[list["ReferralLink"]] = relationship(back_populates="master")
