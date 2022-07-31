import uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine

from app.database.database import engine
from app.models import metadata

from .api.router import api_router

app = FastAPI(title="Employment exchange")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


app.include_router(api_router, prefix="/api")

# if __name__ == "__main__":
#     uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)
