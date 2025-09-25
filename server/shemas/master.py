from pydantic import BaseModel, Field


class MasterCreateSchema(BaseModel):
    specialization: str = Field(..., max_length=100, description="Спеціалізація майстра")
    description: str | None = Field(None, description="Опис майстра")
    experience_years: int = Field(0, ge=0, description="Досвід у роках")
    location: str = Field(..., max_length=100, description="Локація майстра")
    schedule: str = Field(..., description="Розклад роботи (наприклад, Пн-Пт 9:00-18:00)")
    user_id: int = Field(..., description="ID користувача, який є майстром")