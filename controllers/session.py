# app/controllers/session_controller.py
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException
from database.collections import session_collection,car_collection,component_collection
from models.session import Session, SessionResponse, SessionUpdate
from typing import List

def create_session(session: Session) -> SessionResponse:
    # 1️⃣ Verificar que el coche existe
    car = car_collection.find_one({"_id": ObjectId(session.car_id)})
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    # 2️⃣ Fecha por defecto
    session_date = datetime.now()

    session_dict = {
        "heures": session.heures,
        "date": session_date,
        "circuit": session.circuit,
        "climat": session.climat,
        "notes": session.notes,
        "car_id": session.car_id,
    }

    # 3️⃣ Insertar sesión
    result = session_collection.insert_one(session_dict)
    session_id = str(result.inserted_id)

    # 4️⃣ Actualizar horas del coche
    car_collection.update_one(
        {"_id": ObjectId(session.car_id)},
        {"$inc": {"hours": session.heures}}
    )

    # 5️⃣ Actualizar horas de TODOS los componentes del coche
    component_collection.update_many(
        {"car_id": session.car_id},
        {"$inc": {"operating_hours": session.heures}}
    )

    return SessionResponse(
        id=session_id,
        heures=session.heures,
        date=session_date,
        circuit=session.circuit,
        climat=session.climat,
        notes=session.notes,
        car_id=session.car_id,
    )


def get_sessions_by_car(car_id: str) -> List[SessionResponse]:
    sessions = []

    cursor = session_collection.find({"car_id": car_id}).sort("date", -1)

    for doc in cursor:
        sessions.append(
            SessionResponse(
                id=str(doc["_id"]),
                heures=doc["heures"],
                date=doc["date"],
                circuit=doc["circuit"],
                climat=doc["climat"],
                notes=doc.get("notes", ""),
                car_id=doc["car_id"],
            )
        )

    return sessions

def update_session(session_id: str, data: SessionUpdate) -> SessionResponse:
    session = session_collection.find_one({"_id": ObjectId(session_id)})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    update_data = {}

    # 1️⃣ Calcular diferencia de horas (si cambia)
    diff = 0.0
    if data.heures is not None:
        old_heures = session["heures"]
        diff = data.heures - old_heures
        update_data["heures"] = data.heures

    # 2️⃣ Otros campos
    if data.circuit is not None:
        update_data["circuit"] = data.circuit
    if data.climat is not None:
        update_data["climat"] = data.climat
    if data.notes is not None:
        update_data["notes"] = data.notes

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    # 3️⃣ Actualizar sesión
    session_collection.update_one(
        {"_id": ObjectId(session_id)},
        {"$set": update_data}
    )

    # 4️⃣ Aplicar diferencia a coche y componentes
    if diff != 0:
        car_id = session["car_id"]

        car_collection.update_one(
            {"_id": ObjectId(car_id)},
            {"$inc": {"hours": diff}}
        )

        component_collection.update_many(
            {"car_id": car_id},
            {"$inc": {"operating_hours": diff}}
        )

    # 5️⃣ Respuesta actualizada
    updated = session_collection.find_one({"_id": ObjectId(session_id)})

    return SessionResponse(
        id=str(updated["_id"]),
        heures=updated["heures"],
        date=updated["date"],
        circuit=updated["circuit"],
        climat=updated["climat"],
        notes=updated.get("notes", ""),
        car_id=updated["car_id"],
    )


def get_all_sessions() -> List[SessionResponse]:
    sessions_list = []

    cursor = session_collection.find()

    for doc in cursor:
        sessions_list.append(
            SessionResponse(
                id=str(doc["_id"]),
                heures=doc["heures"],
                date=doc["date"],
                circuit=doc["circuit"],
                climat=doc["climat"],
                notes=doc.get("notes", ""),
                car_id=doc["car_id"],
            )
        )


    return sessions_list

