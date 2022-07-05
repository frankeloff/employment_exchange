import datetime

from pydantic import BaseModel, EmailStr, constr


class BaseUser(BaseModel):
    name: str
    email: EmailStr
    is_company: bool = False
    create_at: datetime.datetime
    update_at: datetime.datetime


class UserIn(BaseUser):
    password: constr(min_length=10)

    class Config:
        orm_mode = True


class UserOut(BaseUser):
    id: int

    class Config:
        orm_mode = True
