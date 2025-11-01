from pydantic import BaseModel


class ReferralLinkSchema(BaseModel):
    code: int
    master_tg_id: int
    created_by_tg_id: int
    # bonus_amount: int
    