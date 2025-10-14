from fastapi import APIRouter, Depends, status

from ..db import AsyncDB, ReferralLink
from ..shemas import ReferralLinkSchema

from ..utils import check_master_exists_exception, check_user_exists_exception


referrals_router = APIRouter(prefix='/refferal', tags=['Referral'])


@referrals_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_referral_link(data: ReferralLinkSchema,
                               session = Depends(AsyncDB.get_session)
                               ):
    master = await check_master_exists_exception(data.master_tg_id, session)
    user = await check_user_exists_exception(data.created_by_tg_id, session)

    link = ReferralLink(
        code = user.tg_id,
        master_tg_id = master.tg_id,
        created_by_tg_id = user.tg_id,
        bonus_amount = master.ref_bonus,
    )

    await session.flush()
    session.add(link)

    return link