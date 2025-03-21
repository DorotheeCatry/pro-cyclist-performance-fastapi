from typing import TypedDict

class ResponseData(TypedDict):
    
    message: str
    status : bool
    
class LoginData(TypedDict):
    email : str
    password: str
    
class RegisterData(TypedDict):
    username : str
    email : str
    password : str
    role : int