from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..db import AsyncDB, Master, User


async def get_master_services(tg_id: int, session):
            master = await session.scalar(
                select(Master)
                .join(Master.user)
                .where(User.tg_id == tg_id)
                .options(selectinload(Master.services))
            )
            return master