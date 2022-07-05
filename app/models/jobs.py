import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from . import Base


class Jobs(Base):
    __tablename__ = "Jobs"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String)
    description = Column(String)
    salary_from = Column(Integer)
    salary_to = Column(Integer)
    is_active = Column(Boolean)
    create_at = Column(DateTime(True), default=datetime.datetime.now)
    update_at = Column(DateTime(True), default=datetime.datetime.now)
