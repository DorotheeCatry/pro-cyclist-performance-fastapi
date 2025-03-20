from fastapi import APIRouter, HTTPException
import sqlite3
from app.db.db_utils import get_db_connection
from app.db.athlete import create_athlete
from app.core.security import get_password_hash, verify_password
from app.utils.jwt_handler import create_access_token
from typing import TypedDict

class LoginData(TypedDict):
    email : str
    password: str
    
class RegisterData(TypedDict):
    username : str
    email : str
    password : str
    role : int

router = APIRouter()

# REGISTER USER
@router.post("/register")
def register(data: RegisterData):
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
    hashed_password = get_password_hash(data["password"])
    conn = get_db_connection()
    cursor = conn.cursor()
    successfully_created = False
    response = {"message" : "", "status": 0}
    
    try:
        cursor.execute(
            """INSERT INTO user (username, email, password, role) VALUES (?, ?, ?, ?) RETURNING id""",
            (data["username"], data["email"], hashed_password, data["role"]),
        )
        user_id = cursor.fetchone()["id"]
        
        conn.commit()
        successfully_created = True

    except Exception as e:
        response["message"] = str(e)
        
    finally:
        conn.close()

    if successfully_created:
        response["user"] = {"id": user_id, "username": data["username"], "email": data["email"], "role": data["role"]}
        response["athlete"] = create_athlete(user_id)["message"]
        response["message"] = f"User {data["username"]} successfully created!"
        response["status"] = 1
    
    print(response["message"])
    
    return response

# LOGIN USER
@router.post("/login")
def login(data: LoginData):
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
    
    cursor.execute("SELECT id, username, password, role FROM user WHERE email = ?", (data["email"],))
    user = cursor.fetchone()
    
    conn.close()

    if not user:
        raise HTTPException(status_code=400, detail="Email not found")
    
    if not verify_password(data["password"], user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect password")

    # JWT Creation
    access_token = create_access_token(data={"sub": str(user["id"]), "username": user["username"], "role": user["role"]})

    return {"access_token": access_token, "token_type": "bearer", "user": {"username": user["username"], "role": user["role"], "id": user["id"]}}
