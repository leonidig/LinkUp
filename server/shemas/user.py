from pydantic import BaseModel


class UserSchema(BaseModel):
    tg_id: int
    username: str
    phone: str
    name: str