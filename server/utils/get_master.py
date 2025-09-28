from sqlalchemy import select
from ..db import Master, User


async def get_master_by_tg_id(tg_id: int,
                              session
                            ) -> Master | None:
        return await session.scalar(
            select(Master)
            .join(Master.user)
            .where(User.tg_id == tg_id)
        )