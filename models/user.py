from pydantic import BaseModel, EmailStr
from datetime import datetime

'''
    USER ATTRIBUTES
    - self.id - str - unique identifier of the user
    - self.name - str - name of the user
    - self.email - EmailStr - email of the user
    - self.role - str - role of the user between [admin,client,technician]
    - self.telephone - str - telephone of the user
'''


class User(BaseModel):
    id: str | None = None
    name: str
    email: EmailStr
    role: str
    telephone: str | None = None


    class Config:
        orm_mode = True