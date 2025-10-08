from fastapi import APIRouter, HTTPException
from controllers import component
from models.component import ComponentRequest

router = APIRouter()



@router.post("/composant/")
def create_component(component_request: ComponentRequest):
    return component.create_component(component_request)

@router.get("/composant/{component_qr}")
def get_component(component_qr: str):
    component_new = component.get_component(component_qr)
    if not component_new:
        raise HTTPException(status_code=404, detail="Component not found")
    return component_new
