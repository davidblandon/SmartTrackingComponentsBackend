# app/controllers/user_controller.py
from typing import Optional
from database.collections import user_collection
from utils.user_security import decode_access_token, hash_password, verify_password, create_access_token
from database.collections import user_collection
from fastapi import Depends, HTTPException, status
from models.user import UserCreate, UserResponse, User
from utils.user_type import RoleEnum
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")  # login endpoint to implement later

def get_user_by_email(email: str) -> Optional[User]:
    doc = user_collection.find_one({"email": email})
    if not doc:
        return None
    doc["id"] = str(doc["_id"])
    # map db doc to User model
    return User(
        id=doc["id"],
        name=doc["name"],
        email=doc["email"],
        role=doc.get("role"),
        telephone=doc.get("telephone"),
        hashed_password=doc.get("hashed_password"),
    )

def create_user(user_in: UserCreate) -> UserResponse:
    # check exist
    existing = user_collection.find_one({"email": user_in.email})
    if existing:
        raise ValueError("User with this email already exists")

    hashed = hash_password(user_in.password)
    doc = {
        "name": user_in.name,
        "email": user_in.email,
        "role": user_in.role.value if hasattr(user_in.role, "value") else user_in.role,
        "telephone": user_in.telephone,
        "hashed_password": hashed,
    }
    res = user_collection.insert_one(doc)
    user_id = str(res.inserted_id)
    return UserResponse(
        id=user_id,
        name=user_in.name,
        email=user_in.email,
        role=doc["role"],
        telephone=user_in.telephone,
    )

def get_current_user_from_token(token: str = Depends(oauth2_scheme)) -> User:
    # decode token and find user in DB
    try:
        payload = decode_access_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    subject = payload.get("sub")
    if not subject:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    # subject will be user email (we'll use that)
    user_doc = user_collection.find_one({"email": subject})
    if not user_doc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    user_doc["id"] = str(user_doc["_id"])
    return User(
        id=user_doc["id"],
        name=user_doc["name"],
        email=user_doc["email"],
        role=user_doc.get("role"),
        telephone=user_doc.get("telephone"),
        hashed_password=user_doc.get("hashed_password"),
    )

def admin_required(current_user: User = Depends(get_current_user_from_token)) -> User:
    if current_user.role != RoleEnum.admin.value and current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privilege required")
    return current_user

def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    # OAuth2PasswordRequestForm gives:
    # form_data.username and form_data.password
    user: User = get_user_by_email(form_data.username)

    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = create_access_token(user.email)

    return {"access_token": token, "token_type": "bearer"}