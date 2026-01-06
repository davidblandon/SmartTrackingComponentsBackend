from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

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
    circuit: str
    climat: str 
    notes: str = ""
    car_id: str


    class Config:
        orm_mode = True


class SessionResponse(BaseModel):
    id: str
    heures: float
    session_date: datetime = None
    circuit: str
    climat: str 
    notes: str = ""
    car_id: str

    


class SessionUpdate(BaseModel):
    heures: Optional[float] = None
    circuit: Optional[str] = None
    climat: Optional[str] = None
    notes: Optional[str] = None