import os, json
import qrcode
import hashlib
from fastapi import UploadFile, File, Form, HTTPException
from database.collections import component_collection 
from bson import ObjectId
from models.component import Component, ComponentResponse
from typing import List
from datetime import datetime
from utils.nature import NatureEnum
from typing import Optional, Union
from database.collections import car_collection

QR_FOLDER = "static/components/qrcodes/"
os.makedirs(QR_FOLDER, exist_ok=True)

PHOTOS_FOLDER = "static/components/photos/"
os.makedirs(PHOTOS_FOLDER, exist_ok=True)


def create_component(
    name: str,
    nature: NatureEnum,
    uploaded_file: UploadFile = None,
    operating_hours: float = 0.0,
    commissioning_date: datetime = None,
    decommissioning_date: datetime = None,
    car_id: str = None
) -> ComponentResponse:

    if not uploaded_file:
        raise HTTPException(status_code=400, detail="Photo is required")

    # Guardar la foto
    photo_path = os.path.join(PHOTOS_FOLDER, uploaded_file.filename)
    with open(photo_path, "wb") as buffer:
        buffer.write(uploaded_file.file.read())

    # Crear instancia del modelo
    component = Component(
        name=name,
        photo=photo_path,
        nature=nature,
        operating_hours=operating_hours,
        commissioning_date=commissioning_date,
        decommissioning_date=decommissioning_date,
        car_id=car_id
    )

    # Convertir a dict para Mongo
    component_dict = component.model_dump()
    result = component_collection.insert_one(component_dict)
    component_id_str = str(result.inserted_id)

    # Generar QR
    qr_hash = hashlib.sha256(component_id_str.encode()).hexdigest()
    qr_path = os.path.join(QR_FOLDER, qr_hash + ".png")
    qrcode.make(qr_hash).save(qr_path)

    # Actualizar QR en Mongo
    component_collection.update_one(
        {"_id": ObjectId(component_id_str)},
        {"$set": {"component_qr": qr_hash, "photo": photo_path}}
    )

    # Retornar respuesta
    return ComponentResponse(
        id=component_id_str,
        name=component.name,
        photo=photo_path,
        component_qr=qr_hash,
        nature=component.nature,
        operating_hours=component.operating_hours,
        commissioning_date=component.commissioning_date,
        decommissioning_date=component.decommissioning_date,
        car_id=component.car_id
    )


def get_component(component_qr: str) -> Component:
    component_doc = component_collection.find_one({"component_qr": component_qr})
    if not component_doc:
        return None
    component_doc["id"] = str(component_doc["_id"])
    return ComponentResponse(
        id = component_doc["id"],
        name = component_doc["name"],
        photo = component_doc["photo"],
        component_qr = component_doc["component_qr"],
        nature = component_doc["nature"],
        operating_hours = component_doc.get("operating_hours"),
        commissioning_date = component_doc.get("commissioning_date"),
        decommissioning_date = component_doc.get("decommissioning_date"),
        car_id = component_doc.get("car_id")

    )

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
    uploaded_file: Optional[Union[UploadFile, str]] = File(None),
    car_id: Optional[str] = Form(None)
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

    if car_id is not None:
        update_data["car_id"] = car_id
            
    if update_data: 
        component_collection.update_one({"_id": ObjectId(component_id)}, {"$set": update_data}) 
        updated_doc = component_collection.find_one({"_id": ObjectId(component_id)}) 
        updated_doc["id"] = str(updated_doc["_id"])
            
        return {
            "message": f"Product updated successfully, ID: {updated_doc['id']}"
        }

    

def delete_component(component_qr: str):
    try:
        component_doc = component_collection.find_one({"component_qr": component_qr})

    except:
        raise HTTPException(status_code=400, detail="Invalid component QR format")
    
    if component_doc is None:
        raise HTTPException(status_code=404, detail="Component not found")
    
    os.remove(component_doc["photo"])     
    os.remove(f"static/components/qrcodes/{component_doc['component_qr']}.png") 

     
    result = component_collection.delete_one({"_id": ObjectId(component_doc["_id"])})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Component not found")
    return {"detail": "Component deleted successfully"}

def assign_component_to_car(car_qr: str, component_qr: str):
    # 1️⃣ Buscar carro
    car = car_collection.find_one({"car_qr": car_qr})
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    # 2️⃣ Buscar componente
    component = component_collection.find_one({"component_qr": component_qr})
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")

    # 3️⃣ Validar si ya está asignado
    if component.get("car_id"):
        raise HTTPException(
            status_code=400,
            detail="Component is already assigned to a car"
        )

    # 4️⃣ Asignar componente
    component_collection.update_one(
        {"_id": component["_id"]},
        {
            "$set": {
                "car_id": str(car["_id"]),
                "commissioning_date": datetime.utcnow()
            }
        }
    )

    return {
        "message": "Component successfully assigned to car",
        "component_id": str(component["_id"]),
        "car_id": str(car["_id"])
    }