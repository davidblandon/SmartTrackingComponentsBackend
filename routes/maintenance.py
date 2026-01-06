# app/routes/session.py
from fastapi import APIRouter, Depends
from models.maintenance import Maintenance, MaintenanceResponse, MaintenanceUpdate
from controllers.maintenance import create_maintenance, get_all_maintenances, get_car_maintenances, get_technician_maintenances, update_maintenance
from fastapi import UploadFile, File, Form
from utils.security import role_required
from utils.user_type import RoleEnum
from models.user import User

router = APIRouter()


@router.post("/create",response_model=MaintenanceResponse,status_code=201)
def create_maintenance_route(type: str = Form(...),car_id: str = Form(...),notes: str = Form(""),file: UploadFile = File(None),current_user: User = Depends(role_required([RoleEnum.technician, RoleEnum.admin]))):
    return create_maintenance(type=type,car_id=car_id,technician_id=current_user.id,notes=notes,uploaded_file=file)

@router.get("/all",response_model=list[MaintenanceResponse])
def get_all_maintenances_route( current_user: User = Depends(role_required(RoleEnum.admin))):
    return get_all_maintenances()

@router.get("/car/{car_id}",response_model=list[MaintenanceResponse])
def get_car_maintenances_route(car_id: str):
    return get_car_maintenances(car_id)

@router.get("/technician/{technician_id}",response_model=list[MaintenanceResponse])
def get_technician_maintenances_route(technician_id: str, current_user: User = Depends(role_required([RoleEnum.technician, RoleEnum.admin]))):
    return get_technician_maintenances(technician_id)

@router.put("/update/{maintenance_id}",response_model=MaintenanceResponse)
def update_maintenance_route(maintenance_id: str,type: str | None = Form(None),notes: str | None = Form(None),file: UploadFile = File(None),current_user: User = Depends(role_required([RoleEnum.admin, RoleEnum.technician]))):
    data = MaintenanceUpdate(
        type=type,
        notes=notes
    )

    return update_maintenance(
        maintenance_id=maintenance_id,
        data=data,
        uploaded_file=file
    )