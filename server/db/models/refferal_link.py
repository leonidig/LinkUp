from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .. import Base
from .user import User


class ReferralLink(Base):
    __tablename__ = "referral_links"

    code: Mapped[str] # creator tg_id 
    master_tg_id: Mapped[int] = mapped_column(ForeignKey("masters.id"))
    created_by_tg_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    bonus_amount: Mapped[int] = mapped_column(default=None)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    is_active: Mapped[bool] = mapped_column(default=True)

    master: Mapped['Master'] = relationship(back_populates="referral_links")