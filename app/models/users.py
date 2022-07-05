import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from . import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    email = Column(String, primary_key=True, unique=True)
    name = Column(String)
    password = Column(String)
    is_company = Column(Boolean)
    create_at = Column(DateTime(True), default=datetime.datetime.now)
    update_at = Column(DateTime(True), default=datetime.datetime.now)
