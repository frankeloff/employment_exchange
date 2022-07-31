from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import depends
from app.crud.users import users
from app.schemas.users import UserIn, UserOut

router = APIRouter()


@router.post("/", response_model=UserOut)
async def create_user(
    u: UserIn,
    session: AsyncSession = Depends(depends.get_session),
):
    user = await users.get_by_email(session, email=u.email)
    if user is not None:
        raise HTTPException(status_code=403, detail="User already exist")
    return await users.create(session, u)


@router.delete("/")
async def delete_user(
    email: EmailStr,
    user=Depends(depends.get_current_user),
    session: AsyncSession = Depends(depends.get_session),
):
    db_object = await users.get_by_email(db=session, email=email)
    if not db_object:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.id == db_object.id:
        raise HTTPException(status_code=403, detail="Not enough rights")
    return await users.delete(session, db_object)


@router.patch("/", response_model=UserIn)
async def update_user(
    id: int,
    u: UserIn,
    user=Depends(depends.get_current_user),
    session: AsyncSession = Depends(depends.get_session),
):
    db_object = await users.get_by_id(db=session, id=id)
    if not db_object:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.id == id:
        raise HTTPException(status_code=403, detail="Not enough rights")
    result = await users.update(session, db_object=db_object, update_obj=u)
    return result


@router.get("/", response_model=List[UserOut])
async def get_users(
    limit: int = 100,
    skip: int = 0,
    session: AsyncSession = Depends(depends.get_session),
):
    return await users.get_all(session, limit=limit, skip=skip)


@router.get("/users/me")
async def get_user(user=Depends(depends.get_current_user)):
    return user
