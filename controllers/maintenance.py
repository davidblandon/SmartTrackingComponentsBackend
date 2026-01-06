import os
from datetime import datetime
from bson import ObjectId
from fastapi import UploadFile, HTTPException

from database.collections import maintenance_collection
from models.maintenance import Maintenance, MaintenanceResponse, MaintenanceUpdate

MAINTENANCE_FOLDER = "static/maintenances"
os.makedirs(MAINTENANCE_FOLDER, exist_ok=True)

def create_maintenance(type: str,car_id: str,technician_id: str,notes: str = "",uploaded_file: UploadFile = None
) -> MaintenanceResponse:

    file_path = ""

    if uploaded_file:
        file_path = os.path.join(
            MAINTENANCE_FOLDER,
            uploaded_file.filename
        )
        with open(file_path, "wb") as buffer:
            buffer.write(uploaded_file.file.read())

    maintenance = Maintenance(
        type=type,
        technician_id=technician_id,
        notes=notes,
        files=file_path,
        car_id=car_id,
        maintenance_date=datetime.now()
    )

    result = maintenance_collection.insert_one(
        maintenance.model_dump()
    )

    return MaintenanceResponse(
        id=str(result.inserted_id),
        **maintenance.model_dump()
    )

def get_all_maintenances():
    items = []

    for doc in maintenance_collection.find().sort("maintenance_date", -1):
        items.append(
            MaintenanceResponse(
                id=str(doc["_id"]),
                **doc
            )
        )
    return items

def get_car_maintenances(car_id: str):
    items = []

    for doc in maintenance_collection.find({"car_id": car_id}):
        items.append(
            MaintenanceResponse(
                id=str(doc["_id"]),
                **doc
            )
        )
    return items


def get_technician_maintenances(technician_id: str):
    items = []

    for doc in maintenance_collection.find({"technician_id": technician_id}):
        items.append(
            MaintenanceResponse(
                id=str(doc["_id"]),
                **doc
            )
        )
    return items

def update_maintenance(maintenance_id: str, data: MaintenanceUpdate, uploaded_file: UploadFile | None = None) -> MaintenanceResponse:
    print("maintenance_id:", maintenance_id)
    maintenance = maintenance_collection.find_one(
        {"_id": ObjectId(maintenance_id)}
    )
    print("a")
    print(maintenance)
    if not maintenance:
        raise HTTPException(status_code=404, detail="Maintenance not found")

    update_data = {
        k: v for k, v in data.model_dump().items() if v is not None
    }

    # 📎 si hay nuevo archivo
    if uploaded_file:
        new_file_path = os.path.join(
            MAINTENANCE_FOLDER,
            uploaded_file.filename
        )

        with open(new_file_path, "wb") as buffer:
            buffer.write(uploaded_file.file.read())

        # 🔥 opcional: borrar archivo antiguo
        old_file = maintenance.get("files")
        if old_file and os.path.exists(old_file):
            try:
                os.remove(old_file)
            except Exception:
                pass

        update_data["files"] = new_file_path

    if update_data:
        maintenance_collection.update_one(
            {"_id": ObjectId(maintenance_id)},
            {"$set": update_data}
        )

    updated = maintenance_collection.find_one(
        {"_id": ObjectId(maintenance_id)}
    )

    return MaintenanceResponse(
        id=str(updated["_id"]),
        **updated
    )