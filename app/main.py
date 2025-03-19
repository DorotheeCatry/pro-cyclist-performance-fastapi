from fastapi import FastAPI
from app.api.v1.endpoints import auth, users, stats
from app.db.db_utils import create_db
from pathlib import Path

db = Path("/app/db/users.db")
if not db.is_file():
    create_db()

app = FastAPI(title="Athlete Performance API")

app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(stats.router, prefix="/api/v1", tags=["stats"])