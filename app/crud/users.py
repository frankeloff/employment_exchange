import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.users import Users
from app.schemas.users import UserIn

from .base import BaseCRUD
from .jobs import jobs


class UsersCRUD(BaseCRUD):
    async def create(self, db: AsyncSession, u: UserIn):
        password = u.password
        u.password = hash_password(password)
        db_object = Users(**u.dict())

        db.add(db_object)
        await db.commit()
        await db.refresh(db_object)

        return db_object

    async def update(self, db: AsyncSession, db_object: Users, update_obj: UserIn):
        encoded_object_in = jsonable_encoder(db_object)
        if isinstance(update_obj, dict):
            update_data = update_obj
        else:
            update_data = update_obj.dict()
        update_data["update_at"] = datetime.datetime.now()
        for field in encoded_object_in:
            if field in update_data:
                if field == "password":
                    setattr(db_object, field, hash_password(update_data[field]))
                else:
                    setattr(db_object, field, update_data[field])

        db.add(db_object)
        await db.commit()
        await db.refresh(db_object)

        return db_object

    async def delete(self, db: AsyncSession, db_object: Users):
        jobs_to_delete = await jobs.get_by_user_id(db, db_object.id)

        for i in range(len(jobs_to_delete)):
            await jobs.delete(db, db_object=jobs_to_delete[i])

        await db.delete(db_object)
        await db.commit()
        return True

    async def get_all(self, db: AsyncSession, limit: int = 100, skip: int = 0):
        query = select(Users).limit(limit).offset(skip)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, id: int):
        query = select(Users).where(Users.id == id)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_by_email(self, db: AsyncSession, email: str):
        query = select(Users).where(Users.email == email)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_by_name(self, db: AsyncSession, name: str):
        query = select(Users).where(Users.name == name)
        result = await db.execute(query)
        return result.scalars().first()


users = UsersCRUD()
