from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth import Token
from app.db.db_utils import get_db_connection
from app.core.security import get_password_hash, verify_password
from app.utils.jwt_handler import create_access_token
from pydantic import BaseModel

router = APIRouter()

@router.post("/register/")
def register(username: str, email: str, password: str, role: str):
    hashed_password = get_password_hash(password)
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """INSERT INTO user (username, email, password, role) 
               VALUES (?, ?, ?, ?) RETURNING id""",
            (username, email, hashed_password, 0),
        )
        user_id = cursor.fetchone()["id"]
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    finally:
        conn.close()

    return {"id": user_id, "username": username, "email": email, "role": 0}
    
    
@router.post("/login", response_model=Token)
# en création