from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.db.athlete import create_athlete
from app.db.athlete import modify_athlete
from app.db.selects import get_athlete_by_id
from app.db.test_session import create_session
from app.utils.jwt_handler import verify_token

router = APIRouter()


# @router.post("/users/create")
# def api_create_user(data: dict):
#     result = create_athlete(data)
#     return result["message"]

@router.post("/users/modify_athlete")
def api_modify_ahtlete(id: int, data: dict):
    result = modify_athlete(id, data)
    return result["message"]

@router.post("/users/create_session")
def api_create_session(athlete_id: int, data: dict):
    result = create_session(athlete_id, data)
    return result["message"]

@router.post("/users/get_athlete")
def api_get_athlete_by_id(athlete_id: int):
    result = get_athlete_by_id(athlete_id)
    return result
