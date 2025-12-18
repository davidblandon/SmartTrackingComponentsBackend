from pydantic import BaseModel, Field
from utils.nature import NatureEnum
from datetime import date, datetime
from typing import Optional

'''
    COMPONENT ATTRIBUTES
    - self.product_id - int - unique identifier of the product
    - self.name - str - name of the product
    - self.photo - str - direction of photo of the product
    - self.qr_filename - str - qr of the product
    - self.nature - NatureEnum - nature of the product between [BMS,VCU,DC_dc,Chargeur,Boite_de_jonction,Module_de_batterie,Groupe_moteur_onduleur,moteur,Onduleur]
    DC_dc = "DC/dc"
    Chargeur = "Chargeur"
    Boite_de_jonction = "Boite de jonction"
    Module_de_batterie = "Module de batterie"
    Groupe_moteur_onduleur = "Groupe moteur-onduleur"
    moteur = "moteur"
    Onduleur = "Onduleur"

 ]
    - self.operating_hours - float - operating hours of the product
    - self.commissioning_date - datetime - commissioning date of the product
    - self.decommissioning_date - datetime - decommissioning date of the product
'''




class Component(BaseModel): 
    name: str
    photo: str            
    component_qr: str = ""
    nature: NatureEnum 
    operating_hours: Optional[float] = 0.0
    commissioning_date: Optional[datetime] = None
    decommissioning_date: Optional[datetime] = None
    car_id: Optional[str] = None





    class Config:
        orm_mode = True

    def get_Cars(self):
        pass

    def get_id(self):
        return self.component_id
    
    def get_name(self): 
        return self.name
    
    def get_photo_path(self):
        return self.photo
    
    def get_qr_filename(self):
        return self.qr_filename
    
    def get_nature(self):
        return self.nature  
    
    def get_operating_hours(self):
        return self.operating_hours 
    
    def get_commissioning_date(self):
        return self.commissioning_date
    
    def get_decommissioning_date(self):
        return self.decommissioning_date
    
    def set_decommissioning_date(self, decommissioning_date: datetime):
        self.decommissioning_date = datetime.utcnow()

    def set_commissioning_date(self, commissioning_date: datetime):
        self.commissioning_date = datetime.utcnow()

    def set_name(self, name: str):
        self.name = name

    def set_photo_path(self, photo: str):
        self.photo = photo  



class ComponentResponse(BaseModel):
    id: str
    name: str
    photo: str            
    component_qr: str = ""
    nature: NatureEnum 
    operating_hours: Optional[float] = 0.0
    commissioning_date: Optional[datetime] = None
    decommissioning_date: Optional[datetime] = None
    car_id: Optional[str] = None





