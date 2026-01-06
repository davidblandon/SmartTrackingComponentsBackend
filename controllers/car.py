import os
import qrcode
import hashlib
from fastapi import Form, HTTPException,UploadFile
from database.collections import car_collection, component_collection, user_collection
from bson import ObjectId
from models.car import Car, CarResponse
from models.component import ComponentResponse
from typing import List
from typing import Optional

QR_FOLDER = "static/cars/qrcodes/"
os.makedirs(QR_FOLDER, exist_ok=True)

PHOTOS_FOLDER = "static/cars/photos/"
os.makedirs(PHOTOS_FOLDER, exist_ok=True)



def create_car(
    name: str,
    hours: float,
    owner_id: str,
    uploaded_file: UploadFile = None
) -> CarResponse:


    photo_path = os.path.join(PHOTOS_FOLDER, uploaded_file.filename)
    with open(photo_path, "wb") as buffer:
        buffer.write(uploaded_file.file.read())

    # Crear instancia del modelo
    car = Car(
        name=name,
        hours=hours,
        owner_id=owner_id,
        photo_path=photo_path,
        car_qr=""
    )

    # Convertir a dict para Mongo
    car_dict = car.model_dump()
    result = car_collection.insert_one(car_dict)
    car_id_str = str(result.inserted_id)



    # Generar QR
    qr_hash = hashlib.sha256(car_id_str.encode()).hexdigest()
    qr_path = os.path.join(QR_FOLDER, qr_hash + ".png")
    qrcode.make(qr_hash).save(qr_path)



    # Actualizar QR en Mongo
    car_collection.update_one(
        {"_id": ObjectId(car_id_str)},
        {"$set": {"car_qr": qr_hash}}
    )

    try:
        owner_doc = user_collection.find_one({"_id": ObjectId(owner_id)})
    except:
        raise HTTPException(status_code=404, detail="Client not found")


    # Retornar respuesta
    return CarResponse(
        id=car_id_str,
        name=car.name,
        hours=car.hours,
        owner=owner_doc["name"],
        photo_path=photo_path,  
        car_qr=qr_hash
    )


def get_car(car_qr: str) -> Car:
    car_doc = car_collection.find_one({"car_qr": car_qr})
    if not car_doc:
        return None
    car_doc["id"] = str(car_doc["_id"])
    owner = user_collection.find_one({"_id": ObjectId(car_doc["owner_id"])})["name"]    

    return CarResponse(    id=car_doc["id"],
    name=car_doc["name"],
    hours=car_doc["hours"],            
    photo_path=car_doc["photo_path"],
    owner=owner,
    car_qr=car_doc['car_qr']


def get_all_cars() -> List[Car]:
    cars_list = []

    for car_doc in car_collection.find():
        car_doc["id"] = str(car_doc["_id"])
        owner = user_collection.find_one({"_id": ObjectId(car_doc["owner_id"])})["name"] 
        cars_list.append(CarResponse(id=car_doc["id"],
    name=car_doc["name"],
    hours=car_doc["hours"],            
    photo_path=car_doc["photo_path"],
    owner=owner,
    car_qr=car_doc['car_qr']"
        
    print(cars_list)
        
    return cars_list

def update_car(
    car_id: str,
    name: Optional[str] = Form(None), 
    hours: Optional[float] = Form(None),    
    owner: Optional[str] = Form(None)
                                
):
    car_doc = car_collection.find_one({"_id": ObjectId(car_id)}) 

    if not car_doc:
        raise HTTPException(status_code=404, detail="Car not found") 
    
    update_data = {} 
    if name is not None: 
        update_data["name"] = name 
        
    if hours is not None: 
        update_data["hours"] = hours

    if owner is not None:   
        update_data["owner"] = owner

    

            
    if update_data: 
        car_collection.update_one({"_id": ObjectId(car_id)}, {"$set": update_data}) 
        updated_doc = car_collection.find_one({"_id": ObjectId(car_id)}) 
        updated_doc["id"] = str(updated_doc["_id"])
            
        return {
            "message": f"Car updated successfully, ID: {updated_doc['id']}"
        }

    


def get_coponents(car_id: str)-> List[ComponentResponse]:
    # Validar que el carro exista 
    car = car_collection.find_one({"_id": ObjectId(car_id)}) 

    if not car: 
        raise HTTPException(status_code=404, detail="Car not found") 
    
    # Buscar componentes asociados 
    components_cursor = component_collection.find({"car_id": car_id}) 

    components = [] 
    for comp in components_cursor: 
        comp["id"] = str(comp["_id"]) 
        del comp["_id"] 
        components.append(comp) 
        
    return components

def delete_car(car_qr: str):
    try:
        car_doc = car_collection.find_one({"car_qr": car_qr})

    except:
        raise HTTPException(status_code=400, detail="Invalid car QR format")
    
    if car_doc is None:
        raise HTTPException(status_code=404, detail="car not found")
    
    print(car_doc["photo_path"])
    os.remove(car_doc["photo_path"])     
    os.remove(f"static/cars/qrcodes/{car_doc['car_qr']}.png") 

     
    result = car_collection.delete_one({"_id": ObjectId(car_doc["_id"])})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="car not found")
    return {"detail": "car deleted successfully"}
