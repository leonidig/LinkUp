from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class OrderCreateSchema(BaseModel):
    user_tg_id: int
    master_tg_id: int
    service_id: Optional[int] = None
    description: str
    price: int
    scheduled_at: Optional[datetime] = None


class OrderResponse(BaseModel):
    id: int
    user_id: int
    master_id: int
    service_id: Optional[int]
    description: str
    price: int
    scheduled_at: Optional[datetime]
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
