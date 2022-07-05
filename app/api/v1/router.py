import jwt
from api import depends
from core.const import SECRET_KEY
from core.security import verify_password
from crud.users import users
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from .endpoints import jobs, user

api_router = APIRouter()


@api_router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(depends.get_session),
):
    user = await users.get_by_email(session, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = jwt.encode(jsonable_encoder(user), SECRET_KEY, algorithm="HS256")

    return {"access_token": token, "token_type": "bearer"}


api_router.include_router(user.router, prefix="/users")
api_router.include_router(jobs.router, prefix="/jobs")
