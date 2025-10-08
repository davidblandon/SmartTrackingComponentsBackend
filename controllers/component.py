import os
import qrcode
import hashlib
from fastapi import UploadFile, File, Form, HTTPException
from database.collections import product_collection 
from bson import ObjectId
from models.component import Component


QR_FOLDER = "static/qrcodes/"
os.makedirs(QR_FOLDER, exist_ok=True)

PHOTOS_FOLDER = "static/components_photos/"
os.makedirs(PHOTOS_FOLDER, exist_ok=True)


def create_component(name: str, Uploaded_file=None) -> Component:

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