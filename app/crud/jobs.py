import datetime

from fastapi.encoders import jsonable_encoder
from models.jobs import Jobs
from schemas.jobs import JobIn
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseCRUD


class JobsCRUD(BaseCRUD):
    async def get_all(self, db: AsyncSession, limit: int = 100, skip: int = 0):
        query = select(Jobs).limit(limit).offset(skip)
        result = await db.execute(query)
        return result.scalars().all()

    async def create(self, db: AsyncSession, job: JobIn):
        db_object = Jobs(**job.dict())

        db.add(db_object)
        await db.commit()
        await db.refresh(db_object)

        return db_object

    async def update(self, db: AsyncSession, db_object: Jobs, update_obj: JobIn):
        encoded_object_in = jsonable_encoder(db_object)
        if isinstance(update_obj, dict):
            update_data = update_obj
        else:
            update_data = update_obj.dict()
        update_data["update_at"] = datetime.datetime.utcnow()
        for field in encoded_object_in:
            if field in update_data:
                setattr(db_object, field, update_data[field])

        db.add(db_object)
        await db.commit()
        await db.refresh(db_object)

        return db_object

    async def delete(self, db: AsyncSession, db_object: Jobs):
        await db.delete(db_object)
        await db.commit()

        return True

    async def get_by_id(self, db: AsyncSession, id: int):
        query = select(Jobs).where(Jobs.id == id)
        result = await db.execute(query)
        return result.scalars().first()


jobs = JobsCRUD()
