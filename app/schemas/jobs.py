import datetime
from typing import Optional

from pydantic import BaseModel


class BaseJob(BaseModel):
    user_id: int
    title: str
    description: str
    salary_from: int
    salary_to: int
    is_active: bool = True


class JobIn(BaseJob):
    create_at: datetime.datetime
    update_at: datetime.datetime

    class Config:
        orm_mode = True


class JobOut(BaseJob):
    class Config:
        orm_mode = True
