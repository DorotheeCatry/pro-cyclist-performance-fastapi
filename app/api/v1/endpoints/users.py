from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
# from sqlmodel import Session, select
# from app.models.user import User
# from app.schemas.user import UserRead
# from app.db.db_utils import get_session
from app.db.create_user import create_user
from app.db.modify_athlete import modify_athlete
from app.db.test_session import create_session
from app.utils.jwt_handler import verify_token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

@router.post("/users/create")
def api_create_user(data: dict):
    result = create_user(data)
    return result["message"]

@router.post("/users/modify_athlete")
def api_modify_ahtlete(id: int, data: dict):
    result = modify_athlete(id, data)
    return result["message"]

@router.post("/users/create_session")
def api_create_session(athlete_id: int, data: dict):
    result = create_session(athlete_id, data)
    return result["message"]

# @router.get("/users/me", response_model=UserRead)
# def read_users_me(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
#     payload = verify_token(token)
#     if payload is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Token d'authentification invalide",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     username: str = payload.get("sub")
#     if username is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")
    
#     statement = select(User).where(User.username == username)
#     user = session.exec(statement).first()
#     if user is None:
#         raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
#     return user