from sqlalchemy import select

from ..db import Order


async def filter_orders(user_id: int,
                        session,
                        status: str
                    ):
    query = select(Order).where(Order.user_id == user_id)
    if status != "all":
        query = query.where(Order.status == status)
    result = await session.execute(query)
    return result.scalars().all()