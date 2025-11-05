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
    - self.nature - NatureEnum - nature of the car
    - self.BMS - str - BMS component id
    - self.VCU - str - VCU component id

'''




class Car(BaseModel): 
    name: str
    hours: float            
    owner: str = None
    nature: NatureEnum 
    BMS: str = None
    VCU: str = None

    class Config:
        orm_mode = True


    def get_name(self): 
        return self.name
    
    def get_hours(self):
        return self.hours   
    
    def get_owner(self):
        pass



