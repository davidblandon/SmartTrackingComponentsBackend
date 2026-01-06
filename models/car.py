from typing import Optional
from pydantic import BaseModel, Field
from utils.nature import NatureEnum
from datetime import date, datetime
from database.collections import car_collection

'''
    CAR ATTRIBUTES
    - self-_id - int - unique identifier of the car
    - self.name - str - name of the car
    - self.hours - float - operating hours of the car
    - self.owner - str - id of the owner of the car

    - self.BMS - str - BMS component id
    - self.VCU - str - VCU component id

'''




class Car(BaseModel): 
    name: str
    hours: Optional[float]            
    owner_id: Optional[str] = None
    photo_path: Optional[str] = None
    car_qr: str = ""


    class Config:
        orm_mode = True


    def get_name(self): 
        return self.name
    
    def get_hours(self):
        return self.hours   
    
    def get_owner(self):
        pass




class CarResponse(BaseModel): 
    id: str 
    name: str
    hours: Optional[float]            
    photo_path: Optional[str] = None
    owner: Optional[str] = None
    car_qr: str 

