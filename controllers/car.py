import os
import qrcode
import hashlib
from fastapi import Form, HTTPException
from database.collections import car_collection, component_collection
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
) -> CarResponse:


    # Crear instancia del modelo
    car = Car(
        name=name,
        hours=0.0,
        owner=None,
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

    # Retornar respuesta
    return CarResponse(
        id=car_id_str,
        name=car.name,
        hours=car.hours,
        owner=car.owner,
        car_qr=qr_hash
    )


def get_car(car_qr: str) -> Car:
    car_doc = car_collection.find_one({"car_qr": car_qr})
    if not car_doc:
        return None
    car_doc["id"] = str(car_doc["_id"])
    return Car(**car_doc)

def get_all_cars() -> List[Car]:
    cars_list = []
    for car_doc in car_collection.find():
        car_doc["id"] = str(car_doc["_id"])  
        cars_list.append(Car(**car_doc))

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

    

def delete_car(car_id: str):
    try:
        car_doc = car_collection.find_one({"_id": ObjectId(car_id)})

    except:
        raise HTTPException(status_code=400, detail="Invalid car ID format")
       
    os.remove(f"static/cars/qrcodes/{car_doc['car_qr']}.png") 

     
    result = car_collection.delete_one({"_id": ObjectId(car_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Car not found")
    return {"detail": "Car deleted successfully"}

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