from pydantic import BaseModel, Field
from datetime import date, datetime

'''
    MAINTENANCE ATTRIBUTES
    - self.maintenance_id - int - unique identifier of the maintenance
    - self.date - datetime - date of the maintenance
    - self.type - str - type of the maintenance
    - self.technician - str - technician who performed the maintenance
    - self.notes - str - notes about the maintenance
    - self.files - str - files related to the maintenance
    - self.car - str - car related to the maintenance
    - self.components - str - components related to the maintenance
'''




class Maintenance(BaseModel): 
    date: datetime = None
    type: str
    technician: str 
    notes: str = ""
    files: str = ""
    car: str = ""
    components: str


    class Config:
        orm_mode = True



