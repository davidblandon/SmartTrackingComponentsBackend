from pydantic import BaseModel, Field
from datetime import date, datetime

'''
    SESSION ATTRIBUTES
    - self.session_id - int - unique identifier of the session
    - self.heures - float - hours of the session
    - self.date - datetime - date of the session
    - self.circuit - str - circuit of the session
    - self.climat - str - climate of the session
    - self.notes - str - notes about the session
    - self.car - str - car related to the session

'''




class Session(BaseModel): 
    heures: float
    date: datetime = None
    circuit: str
    climat: str 
    notes: str = ""
    car: str


    class Config:
        orm_mode = True


class SessionResponse(BaseModel):
    id: str
    heures: float
    date: datetime = None
    circuit: str
    climat: str 
    notes: str = ""
    car: str

    
