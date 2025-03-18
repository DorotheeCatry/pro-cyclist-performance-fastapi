from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1.endpoints import auth, users
# from app.db.db_utils import engine
# from sqlmodel import SQLModel

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     SQLModel.metadata.create_all(engine)
#     yield

app = FastAPI(title="ProCyclingAPI")

app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])