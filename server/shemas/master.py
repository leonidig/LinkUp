from pydantic import BaseModel, Field, field_validator
from .user import UserResponse


class MasterCreateSchema(BaseModel):
    specialization: str = Field(..., max_length=18, description="Спеціалізація майстра")
    description: str = Field(min_length=55, max_length=1055, description="Опис майстра")
    experience_years: int = Field(0, ge=0, le=70, description="Досвід у роках")
    location: str = Field(...,min_length=5, max_length=100, description="Локація майстра")
    schedule: str = Field(...,min_length=5, max_length=255, description="Розклад роботи (наприклад, Пн-Пт 9:00-18:00)")
    user_id: int = Field(..., description="ID користувача, який є майстром")

    @field_validator("user_id")
    @classmethod
    def tg_id_length(cls, value: int) -> int:
        if not (6 <= len(str(value)) <= 10):
            raise ValueError("Некорректний формат Telegram ID")
        return value
    

    @field_validator('specialization')
    @classmethod
    def check_specalization(cls, value: str):
        specializations = [
            "Розробник",
            "Будівельник",
            "Дизайнер",
            "Фотограф",
            "Водій",
            "Копірайтер",
            "Майстер по ремонту",
            "Майстер краси",
            "Різноробочий",
            "Репетитор"
        ]
        if value not in specializations:
            raise ValueError(f'Спеціалізація {value} не допустима')
        return value


class MasterResponse(BaseModel):
    specialization: str
    description: str
    experience_years: int
    location: str
    schedule: str
    rating: float
    bad_grades: int
    good_grades: int
    user: UserResponse
    