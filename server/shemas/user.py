from typing import Optional

from pydantic import BaseModel, Field, field_validator, constr


class UserSchema(BaseModel):
    tg_id: int = Field(..., description='User Telegram ID')
    username: Optional[str] = Field(None, description="User Default Name")
    phone: str = Field(..., description='User Phone Number')
    name: str = Field(..., min_length=2, max_length=55, description='User Default Name')


    @field_validator('phone')
    @classmethod
    def check_length(cls, value):
        if len(str(value)) not in [12, 13, 14]:
            raise ValueError('Некорректний формат номера телефона')
        
        return value


    @field_validator("tg_id")
    @classmethod
    def tg_id_length(cls, value: int) -> int:
        if not (6 <= len(str(value)) <= 10):
            raise ValueError("Некорректний формат Telegram ID")
        return value
    

    @field_validator("username")
    @classmethod
    def validate_name(cls, value: Optional[str]) -> Optional[str]:
        if value == "":
            return None
        if value is not None:
            if not (2 <= len(value) <= 55):
                raise ValueError("Юзер-нейм повинно містити від 2 до 55 символів")
        return value
    

class UserResponse(BaseModel):
    tg_id: int
    username: str | None
    phone: str
    name: str