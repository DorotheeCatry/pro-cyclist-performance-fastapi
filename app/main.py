from fastapi import FastAPI
from app.api.v1.endpoints import auth, users, stats
from app.db.db_utils import create_db
from pathlib import Path

db = Path("/app/db/users.db")
if not db.is_file():
    create_db()

app = FastAPI(
    title="Pro Cyclist Performance API",
    description="""
    Welcome to the Pro Cyclist Performance API! 🚴
    
    This API allows you to manage users, track athlete statistics, and analyze performance data.
    Use the endpoints to create accounts, modify athlete information, log training sessions,
    and retrieve key performance insights.
    
    Features:
    - Secure authentication with JWT
    - Athlete performance tracking
    - Advanced statistics (VO2max, power-to-weight ratio)
    
    📌 Explore the interactive documentation at `/docs` or `/redoc`.
    """)

@app.get("/", tags=["Welcome"])
def read_root():
    """Returns API description on the home page."""
    return {
        "Welcome to the Pro Cyclist Performance API! Use this API to manage athletes and analyze performance data."
    }

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(stats.router, prefix="/api/v1/stats", tags=["stats"])
