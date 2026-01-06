# app/controllers/user_controller.py
from typing import Optional
from database.collections import user_collection
from utils.user_security import hash_password, verify_password, create_access_token
from database.collections import user_collection
from fastapi import Depends, HTTPException
from models.user import UserCreate, UserResponse, User
from fastapi.security import OAuth2PasswordRequestForm



# login endpoint to implement later

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




def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    # OAuth2PasswordRequestForm gives:
    # form_data.username and form_data.password
    user: User = get_user_by_email(form_data.username)

    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = create_access_token(user.email)

    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        telephone=user.telephone,
        access_token=token,
        token_type="bearer"
    )

def get_all_clients():
    clients_list = []
    for user_doc in user_collection.find({"role": "client"}):
        user_doc["id"] = str(user_doc["_id"])  
        clients_list.append(UserResponse(
            id=user_doc["id"],
            name=user_doc["name"],
            email=user_doc["email"],
            role=user_doc["role"],
            telephone=user_doc.get("telephone")
        ))

    return clients_list