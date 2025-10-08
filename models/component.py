from pydantic import BaseModel, Field

'''
    COMPONENT ATTRIBUTES
    - self.product_id - int - unique identifier of the product
    - self.name - str - name of the product
    - self.photo - str - direction of photo of the product
    - self.qr_filename - str - qr of the product
'''


class Component(BaseModel): 
    name: str
    photo: str            
    component_qr: str = ""    

    class Config:
        orm_mode = True


    def get_id(self):
        return self.component_id
    
    def get_name(self): 
        return self.name
    
    def get_photo_path(self):
        return self.photo
    
    def get_qr_filename(self):
        return self.qr_filename
    
class ComponentRequest(BaseModel):
    name: str
    photo: str

