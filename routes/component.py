from fastapi import APIRouter, HTTPException, UploadFile, File
from controllers import component


router = APIRouter()



@router.post("/composant/")
def create_component(name : str, Uploaded_file: UploadFile = File(...)):
    return component.create_component(name, Uploaded_file)

@router.get("/composant/{component_qr}")
def get_component(component_qr: str):
    component_new = component.get_component(component_qr)
    if not component_new:
        raise HTTPException(status_code=404, detail="Component not found")
    return component_new
