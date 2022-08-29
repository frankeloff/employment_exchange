from fastapi import FastAPI

from app.database.database import engine
from app.models import metadata

from .api.router import api_router

app = FastAPI(title="Employment exchange")


@app.on_event("startup")
async def startup():
    metadata.bind = engine


app.include_router(api_router, prefix="/api")
