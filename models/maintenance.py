from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

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
    type: str
    technician_id: str 
    notes: str = ""
    files: str = ""
    car_id: str = ""
    maintenance_date: datetime = None



    class Config:
        orm_mode = True



class MaintenanceResponse(BaseModel):
    id: str
    maintenance_date: datetime
    type: str
    technician_id: str 
    notes: str
    files: str
    car_id: str


    class Config:
        orm_mode = True


class MaintenanceUpdate(BaseModel):
    type: Optional[str] = None
    notes: Optional[str] = None