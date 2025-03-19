from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Security, HTTPException
from app.utils.jwt_handler import verify_token
from app.db.db_utils import get_db_connection

# Initialize the password context with bcrypt algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define the OAuth2 scheme for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def get_current_user(token: str = Security(oauth2_scheme)) -> dict:
    """
    Retrieve the user from the JWT token.
    Args:
        token (str): The JWT token to verify.
    Returns:
        dict: Contains user information (id, username, email, etc.).
    Raises:
        HTTPException: If the token is invalid or expired.
    """
    payload = verify_token(token)

    user_id: int = payload.get("sub")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, email, role FROM user WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    conn.close()

    return {"id": user["id"], "username": user["username"], "email": user["email"], "role": user["role"]}