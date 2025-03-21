from fastapi import APIRouter, Depends
from app.db.db_utils import get_db_connection
from app.db.athlete import modify_athlete
from app.db.selects import get_athlete_by_id, get_athlete_sessions, get_athlete_list
from app.db.test_session import create_session
from app.core.security import get_current_user
from app.schemas.schemas import ResponseData

router = APIRouter()

@router.post("/modify_athlete")
def api_modify_ahtlete(id: int, data: dict, current_user: dict= Depends(get_current_user)) -> ResponseData:
    result = modify_athlete(id, data)
    return result

@router.post("/create_session")
def api_create_session(athlete_id: int, data: dict, current_user: dict=Depends(get_current_user)) -> ResponseData:
    result = create_session(athlete_id, data)
    return result

@router.post("/get_athlete")
def api_get_athlete_by_id(athlete_id: int):
    result = get_athlete_by_id(athlete_id)
    return result

@router.get("/get_sessions")
def api_get_session(current_user: dict= Depends(get_current_user)):
    result = get_athlete_sessions(current_user["id"])
    return result

@router.get("/get_sessions_coach")
def api_get_session(athlete_id: int, current_user: dict= Depends(get_current_user)):
    result = get_athlete_sessions(athlete_id)
    return result

@router.get("/get_athlete_list")
def api_get_athlete_list(current_user: dict= Depends(get_current_user)):
    result = get_athlete_list()
    return result

@router.get("/delete_account")
def delete_account(current_user: dict = Depends(get_current_user)):
    """
    Delete a user account by user ID.
    """
    user_id = current_user["id"]
    conn = get_db_connection()
    cursor = conn.cursor()
    conn.execute("PRAGMA foreign_keys = ON;") # Turns on the ON CASCADE deletion scheme.
    
    query = """DELETE FROM user WHERE id = ?"""
    
    cursor.execute(query, (user_id,))
    conn.commit()
    conn.close()
    
    return {"message": "Your account has been successfully deleted."}

