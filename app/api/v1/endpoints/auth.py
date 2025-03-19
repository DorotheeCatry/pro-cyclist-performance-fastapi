from fastapi import APIRouter, HTTPException
import sqlite3
from app.db.db_utils import get_db_connection
from app.db.athlete import create_athlete
from app.core.security import get_password_hash, verify_password
from app.utils.jwt_handler import create_access_token

router = APIRouter()

# REGISTER USER
@router.post("/register")
def register(username: str, email: str, password: str, role: str):
    """
    Register a new user in the database.
    Args:
        username (str): The username of the new user.
        password (str): The password of the new user.
        email (str): The email address of the new user.
        role (str): The role of the new user.
    Returns:
        dict: A dictionary containing the new user's id, username, email, and role.
    Raises:
        HTTPException: If the username or email already exists in the database.
    """
    hashed_password = get_password_hash(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    successfully_created = False
    response = {}
    
    try:
        cursor.execute(
            """INSERT INTO user (username, email, password, role) VALUES (?, ?, ?, ?) RETURNING id""",
            (username, email, hashed_password, role),
        )
        user_id = cursor.fetchone()["id"]
        
        conn.commit()
        successfully_created = True
        
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    finally:
        conn.close()

    if successfully_created:
        response["user"] = {"id": user_id, "username": username, "email": email, "role": role}
        response["athlete"] = create_athlete(user_id)["message"]
    
    return response

# LOGIN USER
@router.post("/login")
def login(email: str, password: str):
    """
    Authenticate a user and generate a JWT token.
    Args:
        email (str): The user's email.
        password (str): The user's password.
    Returns:
        dict: A JWT token if authentication is successful.
    Raises:
        HTTPException: If the email or password is incorrect.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, username, password, role FROM user WHERE email = ?", (email,))
    user = cursor.fetchone()
    
    conn.close()

    if not user:
        raise HTTPException(status_code=400, detail="Email not found")
    
    if not verify_password(password, user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect password")

    # JWT Creation
    access_token = create_access_token(data={"sub": user["id"], "username": user["username"], "role": user["role"]})

    return {"access_token": access_token, "token_type": "bearer"}
