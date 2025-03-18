from fastapi import APIRouter, Depends, HTTPException, status
# from app.schemas.user import UserCreate, UserRead
# from app.schemas.auth import Token
from app.db.db_utils import create_db
from app.core.security import get_password_hash, verify_password
from app.utils.jwt_handler import create_access_token
from pydantic import BaseModel

router = APIRouter()

# @router.post("/register", response_model=UserRead)
# def register(user: UserCreate):
#     pass
# en création

# @router.post("/login", response_model=Token)
 
# en création