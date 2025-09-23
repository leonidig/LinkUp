from pydantic import BaseModel, Field, field_validator


class UserSchema(BaseModel):
    tg_id: int = Field(..., description='User Telegram ID')
    username: str | None = Field(min_length=4, max_length=55, description='Telegram Username')
    phone: int = Field(..., description='User Phone Number')
    name: str = Field(..., min_length=2, max_length=55, description='User Default Name')


    @field_validator('phone')
    @classmethod
    def check_length(cls, value):
        if len(str(value)) != 12:
            raise ValueError('Некорректний формат номера телефона')
        
        return value


    @field_validator("tg_id")
    @classmethod
    def tg_id_length(cls, value: int) -> int:
        if not (6 <= len(str(value)) <= 10):
            raise ValueError("Некорректний формат Telegram ID")
        return value