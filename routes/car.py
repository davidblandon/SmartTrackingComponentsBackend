from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, status
from models.car import Car, CarResponse
from typing import List,Optional
from fastapi import UploadFile, File, Form
from controllers import car as car_controller
from fastapi import Form
from utils.security import admin_required
from models.user import User

router = APIRouter()



@router.post("/create/", response_model=CarResponse, status_code=status.HTTP_201_CREATED)
def create_car_route(name : str,admin: User = Depends(admin_required)):
    return car_controller.create_car(name)

@router.get("/cars", response_model=List[Car])
def get_all_cars(admin: User = Depends(admin_required)):
    cars_list = car_controller.get_all_cars()
    
    if not cars_list:
        raise HTTPException(status_code=404, detail="No cars found")
    
    return cars_list

@router.get("/car/{car_qr}")
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
    admin: User = Depends(admin_required)):


    return car_controller.update_car(car_id,name, hours, owner)

@router.delete("/delete/{car_id}")
def delete_car_route(car_id: str, admin: User = Depends(admin_required)):
    return car_controller.delete_car(car_id)
