from typing import List

import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import depends
from app.core.const import SECRET_KEY
from app.core.security import verify_password
from app.crud.jobs import jobs
from app.crud.users import users
from app.schemas.jobs import JobIn, JobOut

router = APIRouter()


@router.post("/", response_model=JobOut)
async def create_job(
    job: JobIn,
    session: AsyncSession = Depends(depends.get_session),
):
    return await jobs.create(session, job)


@router.delete("/")
async def delete_job(
    id: int,
    user=Depends(depends.get_current_user),
    session: AsyncSession = Depends(depends.get_session),
):
    db_object = await jobs.get_by_id(db=session, id=id)
    if not db_object:
        raise HTTPException(status_code=404, detail="Job not found")
    if not user.id == db_object.user_id:
        raise HTTPException(status_code=403, detail="Not enough rights")

    return await jobs.delete(session, db_object)


@router.patch("/", response_model=JobOut)
async def update_job(
    id: int,
    job: JobIn,
    user=Depends(depends.get_current_user),
    session: AsyncSession = Depends(depends.get_session),
):
    db_object = await jobs.get_by_id(db=session, id=id)
    if not db_object:
        raise HTTPException(status_code=404, detail="Job not found")
    if not user.id == db_object.user_id:
        raise HTTPException(status_code=403, detail="Not enough rights")
    result = await jobs.update(session, db_object=db_object, update_obj=job)
    return result


@router.get("/", response_model=List[JobOut])
async def get_users(
    limit: int = 100,
    skip: int = 0,
    session: AsyncSession = Depends(depends.get_session),
):
    return await jobs.get_all(session, limit=limit, skip=skip)
