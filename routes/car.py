from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, status
from models.car import Car, CarResponse
from typing import List,Optional
from fastapi import UploadFile, File, Form
from controllers import car as car_controller
from fastapi import Form
from utils.security import role_required
from utils.user_type import RoleEnum
from models.user import User
from models.component import ComponentResponse

router = APIRouter()



@router.post("/create/", response_model=CarResponse, status_code=status.HTTP_201_CREATED)
def create_car_route( name: str,hours: float,owner_id: str,uploaded_file: UploadFile = File(...),current_user: User = Depends(role_required([RoleEnum.admin]))):
    return car_controller.create_car(name,hours,owner_id,uploaded_file)

@router.get("/all", response_model=List[CarResponse])
def get_all_cars(current_user: User = Depends(role_required([RoleEnum.admin]))):
    cars_list = car_controller.get_all_cars()

    print(cars_list)
    
    if not cars_list:
        raise HTTPException(status_code=404, detail="No cars found")
    
    return cars_list

@router.get("/{car_qr}")
def get_car_route(car_qr: str):
    car_new = car_controller.get_car(car_qr)
    if not car_new:
        raise HTTPException(status_code=404, detail="Car not found")
    return car_new


@router.put("/update/{car_id}")
def update_car_route(car_id: str,
    name: Optional[str] = Form(None), 
    hours: Optional[float] = Form(None),    
    owner: Optional[str] = Form(None),
    current_user: User = Depends(role_required([RoleEnum.admin]))):


    return car_controller.update_car(car_id,name, hours, owner)

@router.delete("/delete/{car_qr}")
def delete_car_route(car_qr: str, current_user: User = Depends(role_required([RoleEnum.admin]))):
    return car_controller.delete_car(car_qr)

@router.get("/{car_id}/components", response_model=List[ComponentResponse])
def get_components_route(car_id: str, current_user: User = Depends(role_required([RoleEnum.admin, RoleEnum.client]))):
    return car_controller.get_coponents(car_id)

