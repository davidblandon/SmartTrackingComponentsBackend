import os
import qrcode
import hashlib
from database.collections import product_collection 
from bson import ObjectId
from models.component import Component
from models.component import ComponentRequest

QR_FOLDER = "static/qrcodes/"
os.makedirs(QR_FOLDER, exist_ok=True)

def create_component(component_request: ComponentRequest) -> Component:
    component_doc = {
        "name": component_request.name,
        "photo": component_request.photo,
    }
    result = product_collection.insert_one(component_doc)
    component_id_str = str(result.inserted_id)


    hash_object = hashlib.sha256(component_id_str.encode())
    qr_hash = hash_object.hexdigest()


    img = qrcode.make(qr_hash)
    component_qr = qr_hash
    qr_path = os.path.join(QR_FOLDER, component_qr + ".png")
    img.save(qr_path)

    product_collection.update_one(
        {"_id": ObjectId(component_id_str)},
        {"$set": {"component_qr": component_qr}}
    )

    component_doc["id"] = component_id_str
    component_doc["component_qr"] = component_qr
    return Component(**component_doc)

def get_component(component_qr: str) -> Component:
    component_doc = product_collection.find_one({"component_qr": component_qr})
    if not component_doc:
        return None
    component_doc["id"] = str(component_doc["_id"])
    return Component(**component_doc)