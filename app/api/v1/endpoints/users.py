from fastapi import APIRouter, Depends
from app.db.db_utils import get_db_connection
from app.db.athlete import modify_athlete
from app.db.selects import get_athlete_by_id
from app.db.test_session import create_session
from app.core.security import get_current_user

router = APIRouter()

@router.post("/modify_athlete")
def api_modify_ahtlete(id: int, data: dict):
    result = modify_athlete(id, data)
    return result["message"]

@router.post("/create_session")
def api_create_session(athlete_id: int, data: dict):
    result = create_session(athlete_id, data)
    return result["message"]

@router.post("/users/get_athlete")
def api_get_athlete_by_id(athlete_id: int):
    result = get_athlete_by_id(athlete_id)
    return result
@router.post("/delete_account")
def delete_account(current_user: dict = Depends(get_current_user)):
    """
    Delete a user account by user ID.
    """
    user_id = current_user["id"]
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """DELETE FROM user WHERE user_id = ?"""
    
    cursor.execute(query, (user_id,))
    conn.commit()
    return {"message": "Your account has been successfully deleted."}

