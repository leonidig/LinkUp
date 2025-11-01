from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator, Field


class ServiceSchema(BaseModel):
    title: str = Field(..., min_length=20, max_length=122, description='Заголовок для послуги')
    description: str = Field(..., min_length=55, max_length=1055, description='Опис для послуги')
    price: int = Field(..., gt=0, lt=9999999, description='Ціна для послуги')
    master_id: int = Field(..., description='Телеграм ID майстра ')


    @field_validator("master_id")
    @classmethod
    def tg_id_length(cls, value: int) -> int:
        if not (6 <= len(str(value)) <= 10):
            raise ValueError("Некорректний формат Telegram ID")
        return value
    

class ServiceResponse(BaseModel):
    id: int
    master_id: int
    title: str
    description: str
    price: int
    created_at: datetime
    status: str


class ServiceUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=20, max_length=122, description="Заголовок послуги")
    description: Optional[str] = Field(None, min_length=55, max_length=1055, description="Опис послуги")
    price: Optional[int] = Field(None, gt=0, lt=9999999, description="Ціна послуги")
