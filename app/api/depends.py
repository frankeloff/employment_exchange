from typing import AsyncGenerator

import jwt
from core.const import SECRET_KEY
from core.security import oauth2_scheme
from crud.users import users
from database.database import engine
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


async def get_session() -> AsyncGenerator:
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


async def get_current_user(
    db: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user = await users.get_by_id(db, id=payload.get("id"))
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
