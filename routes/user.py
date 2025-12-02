# app/routes/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from controllers import user as user_controller
from models.user import UserCreate, UserResponse, User, TokenResponse
from fastapi.security import OAuth2PasswordRequestForm



router = APIRouter()





@router.post("/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, admin: User = Depends(user_controller.admin_required)):
    """
    Create a new user. Only accessible by users with role 'admin'.
    """
    try:
        created = user_controller.create_user(user_in)
        return created
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return user_controller.login_user(form_data)

