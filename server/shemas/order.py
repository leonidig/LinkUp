from typing import Optional
from datetime import datetime
from pydantic import BaseModel, field_validator, Field


class OrderCreateSchema(BaseModel):
    user_tg_id: int = Field(..., description='User Telegram ID')
    master_tg_id: int = Field(..., description='Master Telegram ID')
    service_id: int = Field(..., description='Service ID')
    description: str = Field(..., description='Description For Order')
    price: int = Field(..., description='Price For Order')
    scheduled_at: Optional[datetime] = None
    deadline: Optional[datetime] = None


    @field_validator("user_tg_id", "master_tg_id")
    @classmethod
    def validate_length(cls, value: int) -> int:
        if not (6 <= len(str(value)) <= 10):
            raise ValueError("Некоректний формат — має бути від 6 до 10 цифр")
        return value

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
