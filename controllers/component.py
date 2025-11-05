import os, json
import qrcode
import hashlib
from fastapi import UploadFile, File, Form, HTTPException
from database.collections import component_collection 
from bson import ObjectId
from models.component import Component
from typing import List
from datetime import datetime
from utils.nature import NatureEnum
from typing import Optional, Union

QR_FOLDER = "static/qrcodes/"
os.makedirs(QR_FOLDER, exist_ok=True)

PHOTOS_FOLDER = "static/components_photos/"
os.makedirs(PHOTOS_FOLDER, exist_ok=True)


def create_component(name: str, nature: NatureEnum, Uploaded_file=None) -> Component:

    if Uploaded_file:
        photo_filename = Uploaded_file.filename
        photo_path = os.path.join(PHOTOS_FOLDER, photo_filename)
        with open(photo_path, "wb") as buffer:
            buffer.write(Uploaded_file.file.read())

    else:
        return HTTPException(status_code=400, detail="Photo is required")

    component_doc = {
        "name": name,
        "photo": photo_path,
        "nature": nature,
    }
    result = component_collection.insert_one(component_doc)
    component_id_str = str(result.inserted_id)


    hash_object = hashlib.sha256(component_id_str.encode())
    qr_hash = hash_object.hexdigest()


    img = qrcode.make(qr_hash)
    component_qr = qr_hash
    qr_path = os.path.join(QR_FOLDER, component_qr + ".png")
    img.save(qr_path)

    component_collection.update_one(
        {"_id": ObjectId(component_id_str)},
        {"$set": {"component_qr": component_qr}}
    )

    component_doc["id"] = component_id_str
    component_doc["component_qr"] = component_qr
    return Component(**component_doc)

def get_component(component_qr: str) -> Component:
    component_doc = component_collection.find_one({"component_qr": component_qr})
    if not component_doc:
        return None
    component_doc["id"] = str(component_doc["_id"])
    return Component(**component_doc)

def get_all_components() -> List[Component]:
    components_list = []
    for component_doc in component_collection.find():
        component_doc["id"] = str(component_doc["_id"])  
        components_list.append(Component(**component_doc))

    return components_list

def update_component(
    component_id: str,
    name: Optional[str] = Form(None), 
    nature: Optional[NatureEnum] = Form(None), 
    operating_hours: Optional[float] = Form(None), 
    commissioning_date: Optional[datetime] = Form(None), 
    decommissioning_date: Optional[datetime] = Form(None),
    uploaded_file: Optional[Union[UploadFile, str]] = File(None) 
):
    component_doc = component_collection.find_one({"_id": ObjectId(component_id)}) 

    if not component_doc:
        raise HTTPException(status_code=404, detail="Component not found") 
    
    update_data = {} 
    if name is not None: 
        update_data["name"] = name 
        
    if uploaded_file is not None and uploaded_file != "": 
        old_photo_path = component_doc.get("photo") 
        if old_photo_path and os.path.exists(old_photo_path): 
            os.remove(old_photo_path) 

        photo_path = os.path.join(PHOTOS_FOLDER, uploaded_file.filename) 
        with open(photo_path, "wb") as buffer: 
            buffer.write(uploaded_file.file.read()) 
        update_data["photo"] = photo_path 
        
    if nature is not None: 
        update_data["nature"] = nature 
            
    if operating_hours is not None: 
        update_data["operating_hours"] = operating_hours 
            
    if commissioning_date is not None: 
        update_data["commissioning_date"] = commissioning_date 
            
    if decommissioning_date is not None: 
        update_data["decommissioning_date"] = decommissioning_date 
            
    if update_data: 
        component_collection.update_one({"_id": ObjectId(component_id)}, {"$set": update_data}) 
        updated_doc = component_collection.find_one({"_id": ObjectId(component_id)}) 
        updated_doc["id"] = str(updated_doc["_id"])
            
        return {
            "message": f"Product updated successfully, ID: {updated_doc['id']}"
        }

    

def delete_component(component_id: str):
    try:
        component_doc = component_collection.find_one({"_id": ObjectId(component_id)})

    except:
        raise HTTPException(status_code=400, detail="Invalid component ID format")
    
    os.remove(component_doc["photo"])     
    result = component_collection.delete_one({"_id": ObjectId(component_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Component not found")
    return {"detail": "Component deleted successfully"}