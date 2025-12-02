from pydantic import BaseModel, EmailStr
from datetime import datetime
from utils.user_type import RoleEnum

'''
    USER ATTRIBUTES
    - self.id - str - unique identifier of the user
    - self.name - str - name of the user
    - self.email - EmailStr - email of the user
    - self.role - str - role of the user between [admin,client,technician]
    - self.telephone - str - telephone of the user
'''

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: RoleEnum
    telephone: str | None = None

class User(BaseModel):
    id: str | None = None
    name: str
    email: EmailStr
    role: str
    telephone: str | None = None
    hashed_password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: RoleEnum
    telephone: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

    class Config:
        orm_mode = True