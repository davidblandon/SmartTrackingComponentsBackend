from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, status
from models.component import Component, ComponentResponse, AssignComponentRequest
from typing import List,Optional, Union
from fastapi import UploadFile, File, Form
from controllers import component as component_controller
from utils.nature import NatureEnum
from datetime import datetime
from fastapi import Form
from utils.security import role_required
from utils.user_type import RoleEnum
from models.user import User

router = APIRouter()



@router.post("/create/", response_model=ComponentResponse, status_code=status.HTTP_201_CREATED)
def create_component_route(name : str, nature: NatureEnum ,Uploaded_file: UploadFile = File(...),current_user: User = Depends(role_required([RoleEnum.admin]))):
    return component_controller.create_component(name, nature, Uploaded_file)

@router.get("/all", response_model=List[Component])
def get_all_components(current_user: User = Depends(role_required([RoleEnum.admin]))):
    components_list = component_controller.get_all_components()
    
    if not components_list:
        raise HTTPException(status_code=404, detail="No components found")
    
    return components_list

@router.get("/{component_qr}")
def get_component_route(component_qr: str):
    component_new = component_controller.get_component(component_qr)
    if not component_new:
        raise HTTPException(status_code=404, detail="Component not found")
    return component_new

@router.put("/update/{component_id}")
def update_component_route(component_id: str,
    name: Optional[str] = Form(None), 
    nature: Optional[NatureEnum] = Form(None), 
    operating_hours: Optional[float] = Form(None), 
    commissioning_date: Optional[datetime] = Form(None), decommissioning_date: Optional[datetime] = Form(None),
    uploaded_file: Optional[Union[UploadFile, str]] = File(None), 
    car_id: Optional[str] = Form(None),
    current_user: User = Depends(role_required([RoleEnum.admin]))):


    return component_controller.update_component(component_id,name, nature, operating_hours, commissioning_date, decommissioning_date, uploaded_file)

@router.delete("/delete/{component_id}")
def delete_component_route(component_id: str,current_user: User = Depends(role_required([RoleEnum.admin]))):
    return component_controller.delete_component(component_id)

@router.post("/assingn-component/")
def assign_component(data: AssignComponentRequest, current_user: User = Depends(role_required([RoleEnum.admin]))):
    return component_controller.assign_component_to_car(
        car_qr=data.car_qr,
        component_qr=data.component_qr
    )