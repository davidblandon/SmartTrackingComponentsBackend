from utils.user_type import RoleEnum
from fastapi import Depends, HTTPException, status
from database.collections import user_collection
from utils.user_security import decode_access_token
from fastapi.security import OAuth2PasswordBearer
from models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")  

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

