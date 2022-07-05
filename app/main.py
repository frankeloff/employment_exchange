import uvicorn
from api.router import api_router
from database.database import engine
from fastapi import FastAPI
from models import metadata
from sqlalchemy import create_engine

app = FastAPI(title="Employment exchange")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)
