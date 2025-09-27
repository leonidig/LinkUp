from fastapi import Depends
from sqlalchemy import select

from ..db import AsyncDB, User, Master


async def check_user_exists(tg_id: int,
                            session = Depends(AsyncDB.get_session)
                        ) -> bool:
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if not user:
        return False
    else:
        return True


async def check_master_exists(tg_id: int, session = Depends(AsyncDB.get_session)) -> bool:
    master = await session.scalar(
        select(Master)
        .join(Master.user)
        .where(User.tg_id == tg_id)
    )
    return master is not None